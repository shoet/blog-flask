from flask import (
    Blueprint,
    render_template,
    current_app,
    cli
)
import click

from apps.app import db
from apps.utils import notify
from apps.admin.models import AdminUser

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/', methods=['GET'])
def index():
    return render_template('admin/index.html')

@admin.cli.command('create-user')
@cli.with_appcontext
@click.argument('username')
@click.argument('email')
@click.argument('password')
def create_user(username, email, password):
    admin_user = AdminUser(
        username=username,
        email=email,
        password=password,
    )
    db.session.add(admin_user)
    db.session.commit()
    notify.slack_post(
        bot_token=current_app.config['NOTIFY_SLACK_BOT_TOKEN'],
        channel=current_app.config['NOTIFY_SLACK_CHANNEL'],
        message=f'Create AdminUser\nusername={username}\nemail={email}\npassword={password}'
    )