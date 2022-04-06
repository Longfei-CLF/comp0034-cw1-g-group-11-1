from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError

from volcano_stats_flask import photos
from volcano_stats_flask.models import Profile

class ProfileForm(FlaskForm):
    """ Class for the profile form """
    username = StringField(label='Username', validators=[DataRequired(message='Username is required')])
    bio = TextAreaField(label='Bio', description='Write something about yourself')
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])
    organization_id = SelectField(label='Enter your organization', validators=[DataRequired(message='Organization is required')], coerce=int)

    def validate_username(self, username):
        profile = Profile.query.filter_by(username=username.data).first()
        if profile is not None:
            raise ValidationError('Username already exists, please choose another username')



