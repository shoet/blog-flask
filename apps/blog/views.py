from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for
)

from apps.app import db
from apps.blog.models import PostItem
from apps.blog.forms import PostForm

blog_app = Blueprint('blog', __name__, static_folder='static', template_folder='templates')


@blog_app.route('/', methods=['GET'])
def index():
    # TODO: post list home
    return render_template('blog/index.html')

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