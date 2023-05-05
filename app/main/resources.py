from http import HTTPStatus

from flask_restful import Resource, reqparse

from app.extensions import api, db
from app.main.models import Url
from app.main.serializers import UrlSchema
from config import Config


class UrlApi(Resource):
    serializer = UrlSchema()

    get_parser = reqparse.RequestParser()
    get_parser.add_argument(
        'short_url', type=str, location='args', required=True, help='Short url code required.',
    )

    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'original_url', type=str, location='form', required=True, help='Original url required.',
    )

    delete_parser = get_parser.copy()

    def get(self):
        args = self.get_parser.parse_args()

        url = Url.query.filter_by(short_url=args.short_url).first_or_404()
        return self.serializer.dump(url), HTTPStatus.OK

    def post(self):
        args = self.post_parser.parse_args()

        url = Url(original_url=args.original_url)
        db.session.add(url)
        db.session.commit()

        return self.serializer.dump(url), HTTPStatus.CREATED

    def delete(self):
        args = self.delete_parser.parse_args()

        url = Url.query.filter_by(short_url=args.short_url).first_or_404()
        db.session.delete(url)
        db.session.commit()

        return {'message': 'Object deleted successfully.'}, HTTPStatus.NO_CONTENT


api.add_resource(UrlApi, '/url/')


class UrlListApi(Resource):
    serializer = UrlSchema(many=True)

    get_parser = reqparse.RequestParser()
    get_parser.add_argument(
        'page', type=int, location='args', required=False, default=1, help='Page number required.',
    )

    def get(self):
        args = self.get_parser.parse_args()

        urls = Url.query.order_by(Url.created_date.desc()).paginate(
            page=args.page,
            per_page=Config.URL_PER_PAGE,
            error_out=False
        )

        return self.serializer.dump(urls), HTTPStatus.OK


api.add_resource(UrlListApi, '/urls/')
