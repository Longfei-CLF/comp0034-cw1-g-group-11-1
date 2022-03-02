from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from volcano_stats_flask.models import User

class SignupForm(FlaskForm):
    first_name = StringField(label='First name', validators=[DataRequired()])
    last_name = StringField(label='Last name', validators=[DataRequired()])
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    
    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')

class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('Existed account')

    def validate_password(self, password, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('Non-existed account')
        if not users.check_password(password.data):
            raise ValidationError('Invalid password')