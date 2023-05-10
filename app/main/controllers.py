from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from app.main import bp
from app.main.forms import ShortenUrlForm
from app.main.models import Url


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = ShortenUrlForm()
    if form.validate_on_submit():
        url = Url.create(original_url=form.original_url.data)

        final_url = url_for('main.redirect_to_url', short_url=url.short_url, _external=True)

        flash('Shortened link successfully created!', 'success')
        return render_template('index.html', form=form, short_url=final_url, user=current_user)

    return render_template('index.html', form=form, user=current_user)


@bp.route('/<short_url>')
def redirect_to_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first_or_404()
    url.increase_visits()
    return redirect(url.original_url)
