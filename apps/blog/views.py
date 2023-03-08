from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    abort,
    Markup,
)

from apps.app import db
from apps.blog.models import PostItem
from apps.blog.forms import PostForm
import markdown

blog_app = Blueprint('blog', __name__, static_folder='static', template_folder='templates')


@blog_app.route('/', methods=['GET'])
def index():
    post_items = (db.session
                    .query(PostItem.id, PostItem.title, PostItem.created_at)
                    .order_by(PostItem.created_at.desc())
                    .all())
    return render_template('blog/index.html', post_items=post_items)


@blog_app.route('/post', methods=['GET', 'POST'])
def post_item():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        is_public = form.is_public.data
        post_item = PostItem(title=title, body=body, is_public=is_public)
        db.session.add(post_item)
        db.session.commit()
        return redirect(url_for('blog.index'))
        
    return render_template('blog/post.html', form=form)


@blog_app.route('/<post_item_id>', methods=['GET'])
def edit_item(post_item_id):
    post_item = db.session.query(PostItem).filter(PostItem.id == post_item_id).first()

    if post_item is None:
        abort(404)
    
    md_content = Markup(markdown.markdown(post_item.body))
    return render_template('blog/edit.html', post_item=post_item, md_content=md_content)