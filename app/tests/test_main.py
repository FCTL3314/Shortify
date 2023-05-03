from http import HTTPStatus

from flask import url_for

from app.main.models import Url
from app.tests import TestUrl
from config import TestConfig

test_url = TestUrl()


def test_index_get(client):
    response = client.get(url_for('main.index'))

    assert response.status_code == HTTPStatus.OK


def test_index_post(client):
    response = client.post(url_for('main.index'), data={'original_url': test_url.original_url})

    url = Url.query.first()

    assert Url.query.count() == 1
    assert response.status_code == HTTPStatus.OK
    assert len(url.short_url) == TestConfig.SHORT_URL_LENGTH


def test_redirect_to_url_get(client):
    url = test_url.create()

    assert url.visits == 0

    path = url_for('main.redirect_to_url', short_url=url.short_url)
    response = client.get(path)

    assert url.visits == 1
    assert response.status_code == HTTPStatus.FOUND
    assert response.request.environ['PATH_INFO'] == path
