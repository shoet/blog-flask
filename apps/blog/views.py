from flask import (
    Blueprint,
    render_template,
    redirect
)

blog_app = Blueprint('blog', __name__, static_folder='static', template_folder='templates')


@blog_app.route('/', methods=['GET'])
def index():
    # TODO: post list home
    return render_template('blog/index.html')