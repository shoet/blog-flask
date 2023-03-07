import os


class BaseConfig():
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG_TB_INTERCEPT_REDIRECTS = False


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

config = {
    'dev': DevConfig,
}
    