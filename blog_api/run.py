import os

from flask import Flask

from blog_api.api.config import config
from blog_api.api import api

env = os.environ.get('local', 'base')

app = Flask(__name__)
app.config.from_object(config[env])

app.register_blueprint(api)
