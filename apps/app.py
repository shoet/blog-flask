import os
from pathlib import Path
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    redirect, 
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

base_dir = Path(__file__).parent.parent

db = SQLAlchemy()
debug_toolbar = DebugToolbarExtension()
login_manager = LoginManager()
# login_manager.login_view = ''
# login_manager.login_message = ''


def get_env_file_name(mode):
    print(f'Running mode: {mode}')
    if mode == 'prod':
        env_file = '.env.prod'
    elif mode == 'dev':
        env_file = '.env.dev'
    elif mode == 'local':
        env_file = '.env.local'
    else:
        raise Exception(f'CONFIGURE_MODE {mode} is invalid')
    return env_file
    

def create_app():
    env_file = Path(base_dir / 'configuration' / get_env_file_name(os.environ.get('CONFIGURE_MODE')))
    if not os.path.exists(env_file):
        raise Exception(f'env file is not found. {env_file}')
    load_dotenv(env_file)

    from apps.config import config

    app = Flask(__name__)

    app.config.from_object(config[os.environ.get('CONFIGURE_MODE')])

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{Path(__file__).parent.parent}/{app.config["LOCAL_DB_PATH"]}'
        
    db.init_app(app)
    Migrate(app, db)
    debug_toolbar.init_app(app)
    login_manager.init_app(app)

    from apps.admin import views as admin_views
    app.register_blueprint(admin_views.admin, url_prefix='/admin')

    from apps.blog import views as blog_views
    app.register_blueprint(blog_views.blog, url_prefix='/') # TODO: 変える

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    return app


def page_not_found(e):
    return render_template('404.html'), 404


def internal_server_error(e):
    return render_template('500.html'), 500

@login_manager.unauthorized_handler
def page_unauthorized():
    return redirect(url_for('blog.index'))