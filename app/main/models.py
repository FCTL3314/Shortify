from datetime import datetime

from app.extensions import db


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(516))
    abbreviated_url = db.Column(db.String(64))
    hash = db.Column(db.String(16), unique=True)
    created_date = db.Column(db.Date, default=datetime.utcnow())

    def __repr__(self):
        return f'{self.created_date} | {self.original_url}'
