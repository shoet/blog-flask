import os

class BaseConfig():
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class DevConfig(BaseConfig):
    pass

config = {
    'dev': DevConfig,
}
    