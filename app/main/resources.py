from http import HTTPStatus

from flask import make_response
from flask_restful import Resource

from app.extensions import db
from app.main.models import Url
from app.main.serializers import ShortUrlSchema, UrlSchema
from app.utils.api import generate_response
from app.utils.decorators import validate_data


class UrlApi(Resource):
    url_serializer = UrlSchema()
    short_url_serializer = ShortUrlSchema()

    @validate_data(short_url_serializer)
    def get(self, data):
        short_url = data.get('short_url')

        url = Url.query.filter_by(short_url=short_url).first_or_404()
        response, status = generate_response(data=self.url_serializer.dump(url), status_code=HTTPStatus.OK)
        return make_response(response, status)

    @validate_data(url_serializer)
    def post(self, data):
        original_url = data.get('original_url')

        url = Url(original_url=original_url)
        db.session.add(url)
        db.session.commit()

        response, status = generate_response(data=self.short_url_serializer.dump(url), status_code=HTTPStatus.CREATED)
        return make_response(response, status)
