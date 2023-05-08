from functools import wraps
from http import HTTPStatus

from flask import make_response, redirect, request, url_for
from flask_login import current_user

from app.utils.api import generate_response


def logout_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_anonymous:
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)

    return decorated_view


def validate_data(serializer):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()

            if errors := serializer.validate(data):
                response, status = generate_response(message=errors, status_code=HTTPStatus.BAD_REQUEST)
                return make_response(response, status)
            else:
                return func(*args, **kwargs, data=data)
        return wrapper
    return inner
