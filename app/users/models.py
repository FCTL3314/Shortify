import os

from flask_login import UserMixin
from slugify import slugify
from sqlalchemy.event import listens_for

from app.common.utils import (create_safe_filename, is_extension_allowed,
                              remove_file, save_media_file)
from app.extensions import bcrypt, db
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
        self.hash_password()
        self.create_slug()

    def hash_password(self):
        self.password = bcrypt.generate_password_hash(self.password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def create_slug(self):
        self.slug = slugify(self.username)

    def update_image(self, image):
        filename = image.filename
        if filename and is_extension_allowed(filename):
            safe_filename = create_safe_filename(filename)
            save_media_file(Config.USERS_MEDIA_DIR, image, safe_filename=safe_filename)

            remove_file(
                os.path.join(Config.UPLOAD_FOLDER, Config.USERS_MEDIA_DIR),
                self.image,
            )
            self.image = safe_filename

            db.session.commit()

    def __repr__(self):
        return f'<{self.username}>'


@listens_for(User, 'before_update')
def change_slug(mapper, connection, target):
    target.create_slug()
