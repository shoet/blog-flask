import os

from flask import (
    Blueprint,
    render_template,
    current_app,
    cli,
    redirect,
    url_for,
    flash
)
from flask_login import login_user
import click

from apps.app import db
from apps.utils import notify
from apps.admin.models import AdminUser
from apps.admin.forms import LoginForm

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/', methods=['GET'])
def index():
    return render_template('admin/index.html')

@admin.route(f'/{os.environ["PAGE_LOGIN_ROUTE"]}', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = AdminUser.query.filter_by(email=login_form.email.data).first()

        if user is not None and user.verify_password(login_form.password.data):
            login_user(user)
            notify.slack_post(
                bot_token=current_app.config['NOTIFY_SLACK_BOT_TOKEN'],
                channel=current_app.config['NOTIFY_SLACK_CHANNEL'],
                message=f'ユーザ[{user.email}]がログインしました。'
            )
            return redirect(url_for('blog.post_item'))

        flash('メールアドレスかパスワードが不正です。')
    return render_template('admin/login.html', form=login_form)
    
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
    if admin_user.is_duplicate_email():
        current_app.logger.error('メールアドレスが重複しています。')
        exit(1)
    db.session.add(admin_user)
    db.session.commit()
    notify.slack_post(
        bot_token=current_app.config['NOTIFY_SLACK_BOT_TOKEN'],
        channel=current_app.config['NOTIFY_SLACK_CHANNEL'],
        message=f'Create AdminUser\nusername={username}\nemail={email}\npassword={password}'
    )