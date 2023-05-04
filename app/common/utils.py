import os
from uuid import uuid1

from werkzeug.utils import secure_filename

from config import Config


def is_extension_allowed(filename):
    return filename.split('.')[-1] in Config.ALLOWED_EXTENSIONS


def create_safe_filename(filename):
    safe_filename = str(uuid1()) + secure_filename(filename)

    path = os.path.join(Config.UPLOAD_FOLDER, safe_filename)
    is_exists = os.path.exists(path)

    if is_exists:
        return create_safe_filename(filename)
    return safe_filename


def remove_file(directory, filename):
    if filename:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            os.remove(path)


def save_media_file(directory, file, **kwargs):
    safe_filename = kwargs.get('safe_filename')
    if not safe_filename:
        filename = file.filename
        safe_filename = create_safe_filename(filename)

    path = os.path.join(Config.UPLOAD_FOLDER, directory)

    if not os.path.exists(path):
        os.makedirs(path)

    file.save(os.path.join(path, safe_filename))
