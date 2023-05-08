from datetime import datetime
from random import choices
from string import ascii_letters, digits

from app.extensions import db
from app.utils.validators import is_object_exists
from config import Config


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(516))
    short_url = db.Column(db.String(Config.SHORT_URL_LENGTH), unique=True)
    visits = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.now())
    updated_date = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_url()

    def generate_short_url(self):
        characters = digits + ascii_letters
        short_url = ''.join(choices(characters, k=Config.SHORT_URL_LENGTH))
        if is_object_exists(self, short_url=short_url):
            return self.generate_short_url()
        return short_url

    def increase_visits(self):
        self.visits += 1
        db.session.commit()

    def __repr__(self):
        return f'<{self.short_url} | {self.visits}>'
