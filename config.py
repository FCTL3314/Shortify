import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Media
    UPLOAD_FOLDER = os.path.join(basedir, 'app/media/')
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Authentication
    LOGIN_DISABLED = True

    # Main
    SHORT_URL_LENGTH = 8


class TestConfig(Config):
    # Security
    WTF_CSRF_ENABLED = False

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
