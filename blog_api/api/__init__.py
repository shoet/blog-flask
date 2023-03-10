from flask import (
    Blueprint,
    jsonify,
    request
)

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return jsonify({'hoge': 'fuga'})

@api.post('/post')
def post():
    print(request.json['hoge'])
    return jsonify({'hoge': 'fuga'})