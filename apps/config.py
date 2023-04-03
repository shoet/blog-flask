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
    GCP_SIGNED_URL_EXPIRATION_HOUR = 1
    GCP_CLOUD_STORAGE_BUCKET_PUBLIC = os.environ.get('GCP_CLOUD_STORAGE_BUCKET_PUBLIC')
    GCP_CLOUD_STORAGE_BUCKET_PRIVATE = os.environ.get('GCP_CLOUD_STORAGE_BUCKET_PRIVATE')
    GCP_CLOUD_STORAGE_IMAGE_PATH = os.environ.get('GCP_CLOUD_STORAGE_IMAGE_PATH')
    LOCAL_DB_PATH = os.environ.get('LOCAL_DB_PATH')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True


class ProdConfig(BaseConfig):
    GCP_CLOUD_STORAGE_CONTENT_PATH = os.environ.get('GCP_CLOUD_STORAGE_CONTENT_PATH_PROD')
    GCP_LITESTREAM_REPLICATE_PATH = os.environ.get('GCP_LITESTREAM_REPLICATE_PATH_PROD')


class DevConfig(BaseConfig):
    GCP_CLOUD_STORAGE_CONTENT_PATH = os.environ.get('GCP_CLOUD_STORAGE_CONTENT_PATH_DEV')
    GCP_LITESTREAM_REPLICATE_PATH = os.environ.get('GCP_LITESTREAM_REPLICATE_PATH_DEV')


class LocalConfig(BaseConfig):
    GCP_CLOUD_STORAGE_CONTENT_PATH = os.environ.get('GCP_CLOUD_STORAGE_CONTENT_PATH_LOCAL')
    GCP_LITESTREAM_REPLICATE_PATH = os.environ.get('GCP_LITESTREAM_REPLICATE_PATH_LOCAL')
    WTF_CSRF_ENABLED = False


config = {
    'prod': ProdConfig,
    'dev': DevConfig,
    'local': LocalConfig,
}
    