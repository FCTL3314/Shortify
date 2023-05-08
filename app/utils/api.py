from functools import wraps

from app.utils.validators import is_valid_status_code


def validate_status_code(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        status_code = kwargs.get('status_code') or kwargs.get('status')
        if not is_valid_status_code(status_code):
            raise ValueError(f'Invalid status code: {status_code}')
        return func(*args, **kwargs)

    return wrapper


@validate_status_code
def generate_response(data: dict = None, message: str | dict = None, status_code: int = None) -> (dict, int):
    if message and not isinstance(message, dict):
        message = {'detail': message}

    response = {
        'data': data,
        'msg': message,
        'status_code': status_code,
    }
    return response, status_code
