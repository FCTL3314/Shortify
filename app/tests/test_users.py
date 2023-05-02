from flask import url_for

from http import HTTPStatus

from app.tests import TestUser
from app.users.models import User

test_user = TestUser()


def test_login_get(client):
    response = client.get(url_for('users.login'))

    assert response.status_code == HTTPStatus.OK


def test_login_post_success(client):
    test_user.create()
    data = {
        'username': test_user.username,
        'password': test_user.password,
    }

    path = url_for('users.login')
    response = client.post(path, data=data)

    assert response.status_code == HTTPStatus.FOUND


def test_login_post_failure(client):
    test_user.create()
    data = {
        'username': test_user.username,
        'password': test_user.wrong_password,
    }

    path = url_for('users.login')
    response = client.post(path, data=data)

    assert response.status_code == HTTPStatus.OK
    assert b'Field must be between 8 and 20 characters long.' in response.data


def test_registration_get(client):
    path = url_for('users.registration')
    response = client.get(path)

    assert response.status_code == HTTPStatus.OK


def test_registration_post_success(client):
    data = {
        'username': test_user.username,
        'email': test_user.email,
        'password': test_user.password,
        'password_confirmation': test_user.password,
    }

    path = url_for('users.registration')
    response = client.post(path, data=data)

    user = User.query.first()

    assert response.status_code == HTTPStatus.FOUND
    assert User.query.count() == 1
    assert user.slug == test_user.slug


def test_registration_post_failure(client):
    data = {
        'username': test_user.username,
        'email': test_user.email,
        'password': test_user.wrong_password,
        'password_confirmation': test_user.wrong_password,
    }

    path = url_for('users.registration')
    response = client.post(path, data=data)

    assert response.status_code == HTTPStatus.OK
    assert not User.query.count()
    assert b'Field must be between 8 and 20 characters long.' in response.data
