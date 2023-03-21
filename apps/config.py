import os

from pathlib import Path

basedir = Path(__file__).parent.parent


class BaseConfig():
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    IMAGE_PATH = str(basedir / 'apps' / 'images')
    NOTIFY_SLACK_BOT_TOKEN = os.environ['NOTIFY_SLACK_BOT_TOKEN']
    NOTIFY_SLACK_CHANNEL = os.environ['NOTIFY_SLACK_CHANNEL']
    APP_TITLE = os.environ['APP_TITLE']

class ProdConfig(BaseConfig):
    PG_HOST = os.environ["PG_HOST_PROD"]
    PG_PORT = os.environ["PG_PORT_PROD"]
    PG_DB = os.environ["PG_DB_PROD"]
    PG_USER = os.environ["PG_USER_PROD"]
    PG_PASSWORD = os.environ["PG_PASSWORD_PROD"]
    PG_SCHEMA = os.environ["PG_SCHEMA_PROD"]

    GCP_CLOUD_SQL_UNIX_SOCKET_DIR = os.environ.get("GCP_CLOUD_SQL_UNIX_SOCKET_DIR_PROD")  
    GCP_CLOUD_SQL_INSTANCE_NAME = os.environ.get("GCP_CLOUD_SQL_INSTANCE_NAME_PROD")  

    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True

class DevConfig(BaseConfig):
    PG_HOST = os.environ["PG_HOST_DEV"]
    PG_PORT = os.environ["PG_PORT_DEV"]
    PG_DB = os.environ["PG_DB_DEV"]
    PG_USER = os.environ["PG_USER_DEV"]
    PG_PASSWORD = os.environ["PG_PASSWORD_DEV"]
    PG_SCHEMA = os.environ["PG_SCHEMA_DEV"]

    GCP_CLOUD_SQL_UNIX_SOCKET_DIR = os.environ.get("GCP_CLOUD_SQL_UNIX_SOCKET_DIR_DEV")  
    GCP_CLOUD_SQL_INSTANCE_NAME = os.environ.get("GCP_CLOUD_SQL_INSTANCE_NAME_DEV")  

    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True

class LocalConfig(BaseConfig):
    PG_HOST = os.environ["PG_HOST_LOCAL"]
    PG_PORT = os.environ["PG_PORT_LOCAL"]
    PG_DB = os.environ["PG_DB_LOCAL"]
    PG_USER = os.environ["PG_USER_LOCAL"]
    PG_PASSWORD = os.environ["PG_PASSWORD_LOCAL"]
    PG_SCHEMA = os.environ["PG_SCHEMA_LOCAL"]

    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
    WTF_CSRF_ENABLED = False

config = {
    'prod': ProdConfig,
    'dev': DevConfig,
    'local': LocalConfig,
}
    