from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
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
            raise ValidationError(
                'An account is already registered for that email address')


class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is None:
            raise ValidationError('Non-existed account')

    def validate_password(self, password):
        users = User.query.filter_by(email=self.email.data).first()
        if users is None:
            raise ValidationError('Non-existed account')
        if not users.check_password(password.data):
            raise ValidationError('Invalid password')


class Profile (FlaskForm):
    first_name = StringField(label='First name', validators=[DataRequired()])
    last_name = StringField(label='Last name', validators=[DataRequired()])
    email = EmailField(label='email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
# class ResetPasswordRequestView(View):
#     """
#     Add the the view function of Reset password
#     """
#     methods = ['GET', 'POST']
#
#     def dispatch_request(self):
#         if current_user.is_authenticated:
#             return redirect(url_for('index'))
#         form = ResetPasswordRequestForm()
#         if form.validate_on_submit():
#             user = User.query.filter_by(email=form.email.data).first()
#             if not user:
#                 flash('This email address has not yet be registered')
#                 return redirect(url_for('reset_password_request'))
#
#             send_password_reset_email(user)
#             flash('please check your email, a reset link was sent to you')
#             return redirect(url_for('login'))
#         return render_template('login/reset_password_request.html', title='Reset password', form=form)

# class ResetPasswordRequestForm(FlaskForm):
#     """
#     Request password sheet
#     """
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Request reset password')
