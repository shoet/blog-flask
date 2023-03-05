from flask import (
    Blueprint,
    render_template
)

admin_app = Blueprint('admin', __name__, template_folder='templates')

@admin_app.route('/', methods=['GET'])
def index():
    return render_template('admin/index.html')