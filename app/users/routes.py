from app.users.resources import UserApi, LoginApi, RegistrationApi
from app.extensions import api

api.add_resource(UserApi, '/users/me/')
api.add_resource(LoginApi, '/users/login/')
api.add_resource(RegistrationApi, '/users/registration/')
