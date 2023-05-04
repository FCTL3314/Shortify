from app.extensions import ma
from app.main.models import Url


class UrlSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Url
        load_instance = True
