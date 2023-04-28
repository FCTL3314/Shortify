from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app.extensions import bcrypt, db, login_manager
from app.users import bp
from app.users.forms import LoginForm, RegistrationForm
from app.users.models import User

from app.common.decorators import logout_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/login/', methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember_me)
            return redirect(url_for('main.index'))

        flash('The entered data is incorrect, please try again.', 'warning')

    return render_template('users/login.html', form=form)


@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password)  # type: ignore
        db.session.add(new_user)
        db.session.commit()

        flash('You have successfully registered!', 'success')

        return redirect(url_for('users.login'))
    return render_template('users/registration.html', form=form)
