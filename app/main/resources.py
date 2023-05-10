from http import HTTPStatus

from flask import make_response
from flask_restful import Resource

from app.main.models import Url
from app.main.serializers import ShortUrlSchema, UrlSchema
from app.utils.api import generate_response
from app.utils.decorators import validate_data


class UrlApi(Resource):
    post_serializer = UrlSchema()
    get_serializer = ShortUrlSchema()

    @validate_data(get_serializer)
    def get(self, data):
        short_url = data.get('short_url')

        url = Url.query.filter_by(short_url=short_url).first_or_404()
        response, status = generate_response(data=self.post_serializer.dump(url), status_code=HTTPStatus.OK)
        return make_response(response, status)

    @validate_data(post_serializer)
    def post(self, data):
        original_url = data.get('original_url')

        url = Url.create(original_url=original_url)

        response, status = generate_response(data=self.get_serializer.dump(url), status_code=HTTPStatus.CREATED)
        return make_response(response, status)
