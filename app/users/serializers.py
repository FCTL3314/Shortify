from marshmallow import fields, validate

from app.extensions import ma
from app.users.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('password',)


class UserUpdateSchema(ma.SQLAlchemyAutoSchema):
    username = fields.Str(required=False, validate=validate.Length(min=4, max=32))
    first_name = fields.Str(required=False, validate=validate.Length(max=64))
    last_name = fields.Str(required=False, validate=validate.Length(max=64))

    class Meta:
        model = User
        exclude = ('password', 'email', 'slug')


class UserLoginSchema(ma.SQLAlchemyAutoSchema):
    username = fields.String(required=True, validate=validate.Length(min=4, max=32))
    password = fields.String(required=True, validate=validate.Length(min=6, max=20))


class UserRegistrationSchema(ma.SQLAlchemyAutoSchema):
    username = fields.String(required=True, validate=validate.Length(min=4, max=32))
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.String(required=True, validate=validate.Length(min=6, max=20))
