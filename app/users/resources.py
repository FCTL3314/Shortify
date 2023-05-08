from http import HTTPStatus

from flask import make_response
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from app.extensions import api, db
from app.users.models import User
from app.users.serializers import (UserLoginSchema, UserRegistrationSchema,
                                   UserSchema, UserUpdateSchema)
from app.users.services import login_user, register_user
from app.utils.api import generate_response
from app.utils.decorators import validate_data
from app.utils.validators import is_object_exists


class UserApi(Resource):
    user_serializer = UserSchema()
    user_update_serializer = UserUpdateSchema()

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        response, status = generate_response(data=self.user_serializer.dump(user), status_code=HTTPStatus.OK)
        return make_response(response, status)

    @jwt_required()
    @validate_data(user_update_serializer)
    def patch(self, data):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        for key, value in data.items():
            if key == 'username':
                if user.username != value and is_object_exists(User, username=value):
                    response, status = generate_response(
                        message={'username': 'A user with this email already exists.'},
                        status_code=HTTPStatus.BAD_REQUEST,
                    )
                    return make_response(response, status)
                else:
                    setattr(user, key, value)
            else:
                setattr(user, key, value)

        db.session.commit()

        response, status = generate_response(data=self.user_update_serializer.dump(user), status_code=HTTPStatus.OK)
        return make_response(response, status)

    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user:
            db.session.delete(user)
            db.session.commit()

            response, status = generate_response(status_code=HTTPStatus.NO_CONTENT)
            return make_response(response, status)
        response, status = generate_response(message='User is not found.', status_code=HTTPStatus.NOT_FOUND)
        return make_response(response, status)


api.add_resource(UserApi, '/users/me/')


class LoginApi(Resource):
    serializer = UserLoginSchema()

    @validate_data(serializer)
    def post(self, data):
        response, status = login_user(data=data)
        return make_response(response, status)


api.add_resource(LoginApi, '/users/login/')


class RegistrationApi(Resource):
    serializer = UserRegistrationSchema()

    @validate_data(serializer)
    def post(self, data):
        response, status = register_user(data=data)
        return make_response(response, status)


api.add_resource(RegistrationApi, '/users/registration/')
