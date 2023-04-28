from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, Length


class ShortenUrlForm(FlaskForm):
    original_url = URLField(
        'original_url',
        validators=[URL(), Length(max=516)],
        render_kw={
            'placeholder': 'Paste the url you want to shorten here...',
            'class': 'input',
        },
    )
    submit = SubmitField('Shorten', render_kw={'class': 'btn btn--shortener'})
