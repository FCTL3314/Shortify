import os
from app.extensions import db
from datetime import datetime, timedelta
from uuid import uuid1

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from config import Config


def is_extension_allowed(filename: str) -> bool:
    return filename.split('.')[-1] in Config.ALLOWED_EXTENSIONS


def create_safe_filename(filename: str) -> str:
    safe_filename = str(uuid1()) + secure_filename(filename)

    path = os.path.join(Config.UPLOAD_FOLDER, safe_filename)
    is_exists = os.path.exists(path)

    if is_exists:
        return create_safe_filename(filename)
    return safe_filename


def remove_file(directory: str, filename: str) -> None:
    if filename:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            os.remove(path)


def save_media_file(directory: str, file: FileStorage, **kwargs) -> None:
    safe_filename = kwargs.get('safe_filename')
    if not safe_filename:
        filename = file.filename
        safe_filename = create_safe_filename(filename)

    path = os.path.join(Config.UPLOAD_FOLDER, directory)

    if not os.path.exists(path):
        os.makedirs(path)

    file.save(os.path.join(path, safe_filename))


def is_object_exists(obj: db.Model, **fields):
    is_exists = obj.query.filter_by(**fields).first()
    return True if is_exists else False


def generate_response(data: dict = None, message: str | list | dict = None, status_code: int = None) -> (dict, int):
    response = {
        'data': data,
        'message': modify_message(message),
        'status_code': status_code,
    }
    return response, status_code


def modify_message(message: str | list | dict) -> dict:
    if type(message) is dict:
        return message
    else:
        return {'detail': message}


def create_token_expiration_date(expiration_minutes: int) -> datetime:
    return datetime.utcnow() + timedelta(minutes=expiration_minutes)
