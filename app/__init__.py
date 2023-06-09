from flask import Flask, send_from_directory

from app.extensions import (api, bcrypt, db, jwt_manager, login_manager, ma,
                            migrate)
from app.main import bp as main_bp
from app.users import bp as users_bp
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    bcrypt.init_app(app)

    login_manager.init_app(app)

    api.init_app(app)
    jwt_manager.init_app(app)

    ma.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp, url_prefix='/users')

    @app.route('/media/<path:filename>/')
    def media(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    return app
