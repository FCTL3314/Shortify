from flask import render_template

from app.users import bp


@bp.route('/login/')
def login():
    return render_template('users/login.html')


@bp.route('/registration/')
def registration():
    return render_template('users/registration.html')
