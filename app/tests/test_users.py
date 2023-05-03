from http import HTTPStatus

from flask import url_for
from flask_login import login_user

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


def test_profile_get(client):
    user = test_user.create()
    login_user(user)

    path = url_for('users.profile', slug=user.slug)
    response = client.get(path)

    assert response.status_code == HTTPStatus.OK


def test_profile_post(client):
    user = test_user.create()
    login_user(user)

    data = {
        'username': 'new username',
        'first_name': 'new first name',
        'last_name': 'new last name',
    }

    assert user.username == test_user.username
    assert user.first_name == test_user.first_name
    assert user.last_name == test_user.last_name

    path = url_for('users.profile', slug=user.slug)
    response = client.post(path, data=data)

    assert response.status_code == HTTPStatus.OK
    assert user.username == data['username']
    assert user.first_name == data['first_name']
    assert user.last_name == data['last_name']
