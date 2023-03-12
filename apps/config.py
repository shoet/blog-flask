import os

from pathlib import Path

basedir = Path(__file__).parent.parent


class BaseConfig():
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    IMAGE_PATH = str(basedir / 'apps' / 'images')
    NOTIFY_SLACK_BOT_TOKEN = os.environ['NOTIFY_SLACK_BOT_TOKEN']
    NOTIFY_SLACK_CHANNEL = os.environ['NOTIFY_SLACK_CHANNEL']


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=(
        f'postgresql://{os.environ["PG_HOST_DEV"]}:' 
        + f'{os.environ["PG_PORT_DEV"]}/'
        + f'{os.environ["PG_DB_DEV"]}?' 
        + f'user={os.environ["PG_USER_DEV"]}&'
        + f'password={os.environ["PG_PASSWORD_DEV"]}&'
        + f'options=-c%20search_path={os.environ["PG_SCHEMA_DEV"]}')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=(
        f'postgresql://{os.environ["PG_HOST_TEST"]}:' 
        + f'{os.environ["PG_PORT_TEST"]}/'
        + f'{os.environ["PG_DB_TEST"]}?' 
        + f'user={os.environ["PG_USER_TEST"]}&'
        + f'password={os.environ["PG_PASSWORD_TEST"]}&'
        + f'options=-c%20search_path={os.environ["PG_SCHEMA_TEST"]}')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
    WTF_CSRF_ENABLED = False

config = {
    'dev': DevConfig,
    'test': TestConfig,
}
    