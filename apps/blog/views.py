import os
import uuid
from pathlib import Path
import html

from bs4 import BeautifulSoup
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    abort,
    Markup,
    current_app,
    send_from_directory
)
from flask_login import login_required
import markdown

from apps.app import db
from apps.blog.models import PostItem, PostTag
from apps.blog.forms import PostForm
from apps.utils.gcp import GCP_UTIL

blog = Blueprint('blog', __name__, static_folder='static', template_folder='templates')

def unmark(body):
    html_str = markdown.markdown(body)
    text = ''.join(BeautifulSoup(html_str).findAll(text=True))
    unescaped_text = html.unescape(text) 
    return unescaped_text

def save_thumbnail_image(image):
    file = image.data
    ext = Path(file.filename).suffix
    image_uuid_file_name = str(uuid.uuid4()) + ext
    image_path = Path(current_app.config['IMAGE_PATH'], 'thumbnail' ,image_uuid_file_name)
    file.save(image_path)
    return image_uuid_file_name

@blog.route('/', methods=['GET'])
def index():
    post_items = (db.session
                    .query(PostItem)
                    .outerjoin(PostTag, PostItem.id == PostTag.post_id)
                    .order_by(PostItem.created_at.desc())
                    .all())
    return render_template('blog/index.html', post_items=post_items)


@blog.route('/images/<string:filename>', methods=['GET'])
def thumbnail_image_file(filename):
    print(filename)
    return send_from_directory(Path(current_app.config['IMAGE_PATH'], 'thumbnail'), filename)


@blog.app_template_filter()
def thumbnail_image_file_storage_public(image_file_name):
    url = ('https://storage.googleapis.com/' +
            current_app.config["GCP_CLOUD_STORAGE_BUCKET_PUBLIC"] + '/' + 
            current_app.config["GCP_CLOUD_STORAGE_IMAGE_PATH"] + '/' +
            image_file_name
            )
    return url


def split_tags(tag):
    tag_obj = []
    for t in tag.split(','):
        tag_obj.append(PostTag(tag_name=t))
    return tag_obj


def save_to_storage(form):
    gcp = GCP_UTIL(credential_path=current_app.config.get('GCP_CREDENTIALS_PATH'))
    storage_path_uuid = str(uuid.uuid4())

    thumbnail_image_file_name = storage_path_uuid + Path(form.thumbnail_image.data.filename).suffix
    gcp.upload_storage(
        current_app.config.get('GCP_CLOUD_STORAGE_BUCKET_PUBLIC'), 
        os.path.join(
            current_app.config.get('GCP_CLOUD_STORAGE_IMAGE_PATH'), 
            thumbnail_image_file_name), 
        form.thumbnail_image.data.stream.read())

    content_file_name = storage_path_uuid + '.md'
    gcp.upload_storage(
        current_app.config.get('GCP_CLOUD_STORAGE_BUCKET_PRIVATE'), 
        os.path.join(
            current_app.config.get('GCP_CLOUD_STORAGE_CONTENT_PATH'), 
            content_file_name), 
        form.body.data)
    return thumbnail_image_file_name, content_file_name


@blog.route(f'/{os.environ["PAGE_POST_ITEM_ROUTE"]}', methods=['GET', 'POST'])
@login_required
def post_item():
    form = PostForm()
    # TODO: 画像の差し込みについて
    '''
    一旦保留。
    投稿画面に一時保存
    '''
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        body = form.body.data
        description = unmark(body)[:30]
        thumbnail_image_file_name, content_file_name = save_to_storage(form)
        is_public = form.is_public.data
        post_tags = split_tags(form.tag.data)
        post_item = PostItem(
            title=title, 
            body='', # TODO
            description=description,
            category=category,
            is_public=is_public,
            thumbnail_image_name=thumbnail_image_file_name,
            post_tags=post_tags,
            content_file_name=content_file_name,
            )
        db.session.add(post_item)
        db.session.commit()
        return redirect(url_for('blog.index'))
        
    return render_template('blog/post.html', form=form)


@blog.route('/activities/<int:post_item_id>', methods=['GET'])
def edit_item(post_item_id):
    post_item = db.session.query(PostItem).filter(PostItem.id == post_item_id).first()

    if post_item is None:
        abort(404)
    
    gcp = GCP_UTIL(credential_path=current_app.config.get('GCP_CREDENTIALS_PATH'))
    body = gcp.download_storage_to_bytes(
        current_app.config.get('GCP_CLOUD_STORAGE_BUCKET_PRIVATE'),
        os.path.join(current_app.config.get('GCP_CLOUD_STORAGE_CONTENT_PATH'), post_item.content_file_name)
    ).decode('utf-8')

    md_content = Markup(markdown.markdown(body, extensions=['fenced_code']))
    return render_template('blog/detail.html', post_item=post_item, md_content=md_content)