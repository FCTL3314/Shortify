from flask import render_template

from app.main import bp
from app.main.forms import ShortenUrlForm


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = ShortenUrlForm()
    return render_template('index.html', form=form)
