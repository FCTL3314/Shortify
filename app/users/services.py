from http import HTTPStatus

from flask_jwt_extended import create_access_token

from app.extensions import db
from app.users.models import User
from app.users.serializers import UserSchema
from app.utils.api import generate_response
from app.utils.validators import is_object_exists


def register_user(data):
    serializer = UserSchema()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    errors = dict()

    if is_object_exists(User, username=username):
        errors['username'] = 'User with that username already exists.'
    if is_object_exists(User, email=email):
        errors['email'] = 'User with that email already exists.'

    if errors:
        return generate_response(message=errors, status_code=HTTPStatus.BAD_REQUEST)

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return generate_response(data=serializer.dump(new_user), status_code=HTTPStatus.CREATED)


def login_user(data):
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return generate_response(
            data={'access_token': create_access_token(identity=user.id)},
            status_code=HTTPStatus.CREATED,
        )

    return generate_response(
        message='Could not find a user with the same username and password.',
        status_code=HTTPStatus.BAD_REQUEST,
    )
