from flask_wtf.file import FileField, FileAllowed
from volcano_stats_flask.static import img

photo = FileField('Profile picture', validators=[FileAllowed(img, 'Images only!')])



