import os
from uuid import uuid1

from flask_login import UserMixin
from slugify import slugify
from sqlalchemy.event import listens_for
from werkzeug.utils import secure_filename

from app.extensions import db
from config import Config


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    image = db.Column(db.Text, nullable=True, unique=True)
    slug = db.Column(db.String(32), nullable=False, unique=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_slug()

    def create_slug(self):
        self.slug = slugify(self.username)

    def update_image_if_exists(self, image):
        filename = image.filename
        if filename:
            safe_filename = self.create_safe_filename(filename)
            save_path = os.path.join(Config.UPLOAD_FOLDER, safe_filename)
            image.save(save_path)

            self.remove_old_image(self.image)
            self.image = safe_filename

            db.session.commit()

    def create_safe_filename(self, filename):
        safe_filename = str(uuid1()) + secure_filename(filename)

        path = os.path.join(Config.UPLOAD_FOLDER, safe_filename)
        is_exists = os.path.exists(path)

        if is_exists:
            return self.create_safe_filename(filename)
        return safe_filename

    @staticmethod
    def remove_old_image(filename):
        path = os.path.join(Config.UPLOAD_FOLDER, filename)
        if os.path.exists(path):
            os.remove(path)

    def __repr__(self):
        return self.username


@listens_for(User, 'before_update')
def change_slug(mapper, connection, target):
    target.create_slug()
