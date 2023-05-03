from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user

from app.common.decorators import logout_required
from app.extensions import db, login_manager
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
        if form.authenticate_user():
            return redirect(url_for('main.index'))
        else:
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
        form.create_new_user()
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
        image = form.image.data

        if image:
            user.update_image(image)
        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        db.session.commit()

        flash('Profile successfully updated!', 'success')

    return render_template('users/profile.html', form=form, user=user)
