from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.common.decorators import logout_required
from app.extensions import bcrypt, db, login_manager
from app.users import bp
from app.users.forms import LoginForm, ProfileForm, RegistrationForm
from app.users.models import User


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

        new_user = User(username=username, email=email, password=hashed_password)  # Type: ignore
        db.session.add(new_user)
        db.session.commit()

        flash('You have successfully registered!', 'success')

        return redirect(url_for('users.login'))
    return render_template('users/registration.html', form=form)


@bp.route('/profile/<string:slug>/', methods=['GET', 'POST'])
@login_required
def profile(slug):
    user = User.query.filter_by(slug=slug).first_or_404()

    if user != current_user:
        return abort(403)

    form = ProfileForm()

    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        image = request.files.get('image')

        user.save_image_if_exists(image)

        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        db.session.commit()

        flash('Profile successfully updated!', 'success')

    return render_template('users/profile.html', form=form, user=user)
