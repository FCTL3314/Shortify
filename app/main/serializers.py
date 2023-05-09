from marshmallow import fields, validate

from app.extensions import ma
from config import Config


class UrlSchema(ma.Schema):
    original_url = fields.Url(required=True, validate=validate.Length(max=516))


class ShortUrlSchema(ma.Schema):
    short_url = fields.Str(required=True, validate=validate.Length(max=Config.SHORT_URL_LENGTH))
