import pytest

from app import create_app
from app.extensions import db
from config import TestConfig


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    app_context = app.test_request_context()
    app_context.push()

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
