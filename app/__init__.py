from flask import Flask

from app.extensions import bcrypt, db, login_manager
from app.main.controllers import bp as main_bp
from app.users.controllers import bp as users_bp
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp, url_prefix='/users')

    return app
