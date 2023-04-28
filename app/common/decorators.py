from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def logout_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_anonymous:
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)

    return decorated_view
