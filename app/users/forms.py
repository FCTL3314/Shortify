from flask_login import current_user, login_user
from flask_wtf import FlaskForm
from wtforms import (BooleanField, EmailField, FileField, PasswordField,
                     StringField, SubmitField)
from wtforms.validators import (Email, EqualTo, InputRequired, Length,
                                ValidationError)

from app.common.utils import is_object_exists
from app.extensions import db
from app.users.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'username',
        validators=[InputRequired(), Length(min=4, max=32)],
        render_kw={
            'class': 'input input--auth',
            'placeholder': 'Enter username',
        },
    )
    email = EmailField(
        'email',
        validators=[InputRequired(), Email()],
        render_kw={
            'class': 'input input--auth',
            'placeholder': 'Enter email',
        },
    )
    password = PasswordField(
        'password',
        validators=[
            InputRequired(),
            Length(min=8, max=20),
            EqualTo('password_confirmation', message='Passwords do not match.'),
        ],
        render_kw={
            'class': 'input input--auth',
            'placeholder': 'Enter password',
        },
    )
    password_confirmation = PasswordField(
        'password_confirmation',
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={
            'class': 'input input--auth',
            'placeholder': 'Enter password',
        },
    )
    submit = SubmitField('Sign Up', render_kw={'class': 'btn btn--form'})

    def validate_username(self, username):
        if is_object_exists(User, username=username.data):
            raise ValidationError('A user with this username already exists.')

    def validate_email(self, email):
        if is_object_exists(User, email=email.data):
            raise ValidationError('A user with this email already exists.')

    def create_new_user(self):
        username = self.username.data
        email = self.email.data
        password = self.password.data

        new_user = User(username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()


class LoginForm(FlaskForm):
    username = StringField(
        'username',
        validators=[InputRequired(), Length(min=4, max=32)],
        render_kw={
            'class': 'input input--auth',
            'placeholder': 'Enter username',
        },
    )
    password = PasswordField(
        'password',
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={
            'class': 'input input--auth',
            'placeholder': 'Enter password',
        },
    )
    remember_me = BooleanField(
        'remember_me',
        render_kw={'class': 'form__checkbox'},
    )
    submit = SubmitField('Log In', render_kw={'class': 'btn btn--form'})

    def authenticate_user(self):
        user = User.query.filter_by(username=self.username.data).first()

        if user and user.check_password(self.password.data):
            login_user(user, remember=self.remember_me.data)
            return True
        return False


class ProfileForm(FlaskForm):
    username = StringField(
        'username',
        validators=[Length(min=4, max=32)],
        render_kw={
            'class': 'input input--profile',
            'placeholder': 'Enter username',
        },
    )

    first_name = StringField(
        'first_name',
        validators=[Length(max=64)],
        render_kw={
            'class': 'input input--profile',
            'placeholder': 'Enter first name',
        },
    )

    last_name = StringField(
        'last_name',
        validators=[Length(max=64)],
        render_kw={
            'class': 'input input--profile',
            'placeholder': 'Enter last name',
        },
    )

    image = FileField('image')

    submit = SubmitField('Change', render_kw={'class': 'btn btn--profile'})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user != current_user:
            raise ValidationError('A user with this username already exists.')
