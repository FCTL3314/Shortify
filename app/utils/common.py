import os
from datetime import datetime, timedelta
from uuid import uuid1

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from config import Config


def create_expiration_date(expiration_minutes: int) -> datetime:
    return datetime.utcnow() + timedelta(minutes=expiration_minutes)


def remove_file(directory: str, filename: str) -> None:
    if filename:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            os.remove(path)


def save_media_file(directory: str, file: FileStorage, safe_filename: str = None) -> None:
    if not safe_filename:
        filename = file.filename
        safe_filename = create_safe_filename(filename)

    path = os.path.join(Config.UPLOAD_FOLDER, directory)

    if not os.path.exists(path):
        os.makedirs(path)

    file.save(os.path.join(path, safe_filename))


def create_safe_filename(filename: str) -> str:
    safe_filename = str(uuid1()) + secure_filename(filename)

    path = os.path.join(Config.UPLOAD_FOLDER, safe_filename)
    is_exists = os.path.exists(path)

    if is_exists:
        return create_safe_filename(filename)
    return safe_filename
