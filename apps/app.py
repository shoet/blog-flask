import os
from pathlib import Path
from dotenv import load_dotenv
from flask import (
    Flask,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension

from apps.config import config

base_dir = Path(__file__).parent.parent
if not os.path.exists(Path(base_dir, '.env')):
    raise Exception('.env file is not found.')
load_dotenv()

db = SQLAlchemy()
debug_toolbar = DebugToolbarExtension()

def create_app(env):
    app = Flask(__name__)

    app.config.from_object(config[env])

    db.init_app(app)
    Migrate(app, db)
    debug_toolbar.init_app(app)

    from apps.admin import views as admin_views
    app.register_blueprint(admin_views.admin_app, url_prefix='/admin')

    from apps.blog import views as blog_views
    app.register_blueprint(blog_views.blog_app, url_prefix='/blog') # TODO: 変える

    # TODO: 404, 500

    return app