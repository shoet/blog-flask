import pytest

from apps.app import create_app, db
from apps.blog.models import PostItem, PostTag

@pytest.fixture
def fixture_app():
    app = create_app('test')

    app.app_context().push()

    with app.app_context():
        db.create_all()

    yield app

    PostTag.query.delete()
    PostItem.query.delete()

    db.session.commit()

@pytest.fixture
def client(fixture_app):
    return fixture_app.test_client()
