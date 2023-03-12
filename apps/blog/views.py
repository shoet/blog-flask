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

from apps.app import db
from apps.blog.models import PostItem
from apps.blog.forms import PostForm
import markdown

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

def save_file_remote():
    # TODO: ストレージサービス
    pass

def send_from_remote_file():
    # TODO: ストレージサービス
    pass

@blog.route('/', methods=['GET'])
def index():
    post_items = (db.session
                    .query(
                        PostItem.id,
                        PostItem.title,
                        # PostItem.post_tags, # TODO
                        PostItem.description,
                        PostItem.category,
                        PostItem.thumbnail_image_name,
                        PostItem.created_at,
                        )
                    .order_by(PostItem.created_at.desc())
                    .all())
    return render_template('blog/index.html', post_items=post_items)


@blog.route('/images/<filename>', methods=['GET'])
def thumbnail_image_file(filename):
    print(filename)
    return send_from_directory(Path(current_app.config['IMAGE_PATH'], 'thumbnail'), filename)


def unmark(body):
    html_str = markdown.markdown(body)
    text = ''.join(BeautifulSoup(html_str).findAll(text=True))
    unescaped_text = html.unescape(text) 
    return unescaped_text


@blog.route('/post', methods=['GET', 'POST'])
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
        thumbnail_image_name = save_thumbnail_image(form.thumbnail_image)
        is_public = form.is_public.data
        post_item = PostItem(
            title=title, 
            body=body, 
            description=description,
            category=category,
            is_public=is_public,
            thumbnail_image_name=thumbnail_image_name,
            )
        db.session.add(post_item)
        db.session.commit()
        return redirect(url_for('blog.index'))
        
    return render_template('blog/post.html', form=form)


@blog.route('/<post_item_id>', methods=['GET'])
def edit_item(post_item_id):
    post_item = db.session.query(PostItem).filter(PostItem.id == post_item_id).first()

    if post_item is None:
        abort(404)
    
    md_content = Markup(markdown.markdown(post_item.body))
    return render_template('blog/edit.html', post_item=post_item, md_content=md_content)