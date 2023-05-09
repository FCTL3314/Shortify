from app.main.resources import UrlApi
from app.extensions import api

api.add_resource(UrlApi, '/url/')
