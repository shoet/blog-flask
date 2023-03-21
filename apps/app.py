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

from apps.config import config

base_dir = Path(__file__).parent.parent
if not os.path.exists(Path(base_dir, '.env')):
    raise Exception('.env file is not found.')
load_dotenv()

db = SQLAlchemy()
debug_toolbar = DebugToolbarExtension()
login_manager = LoginManager()
# login_manager.login_view = ''
# login_manager.login_message = ''


def get_conn_pg8000(unix_sock ,user, password, database, schema):
    # set default schema
    import pg8000
    def wrapper():
        conn = pg8000.connect(unix_sock=unix_sock, user=user, password=password, database=database) 
        cursor = conn.cursor()
        cursor.execute(f'set search_path to "{schema}";')
        return conn
    return wrapper


def create_app(env):
    app = Flask(__name__)

    app.config.from_object(config[env])

    if app.config.get('GCP_CLOUD_SQL_UNIX_SOCKET_DIR') is not None and app.config.get('GCP_CLOUD_SQL_INSTANCE_NAME') is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
        creator = get_conn_pg8000(
            unix_sock=f'{app.config["GCP_CLOUD_SQL_UNIX_SOCKET_DIR"]}/{app.config["GCP_CLOUD_SQL_INSTANCE_NAME"]}/.s.PGSQL.5432',
            user=app.config['PG_USER'],
            password=app.config['PG_PASSWORD'],
            database=app.config['PG_DB'],
            schema=app.config['PG_SCHEMA']
        )
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'creator': creator}
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
                                            f'postgresql://{app.config["PG_HOST"]}:'+
                                            f'{app.config["PG_PORT"]}/'+
                                            f'{app.config["PG_DB"]}?'+
                                            f'user={app.config["PG_USER"]}&'+
                                            f'password={app.config["PG_PASSWORD"]}&'+
                                            f'options=-c%20search_path={app.config["PG_SCHEMA"]}')
        
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