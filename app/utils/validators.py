from app import db
from config import Config


def is_valid_status_code(status_code: int) -> bool:
    if not isinstance(status_code, int) or not 100 <= status_code <= 511:
        return False
    return True


def is_object_exists(obj: db.Model, **fields) -> bool:
    is_exists = obj.query.filter_by(**fields).first()
    return True if is_exists else False


def is_extension_allowed(filename: str) -> bool:
    return filename.split('.')[-1] in Config.ALLOWED_EXTENSIONS
