from flask import Blueprint, render_template, flash
from flask_login import current_user

from flask_wtf.file import FileField, FileAllowed
from volcano_stats_flask.static import img
from flask_login import login_required
from flask import request, redirect, url_for



# main_bp = Blueprint('main', __name__, url_prefix='/main')
main_bp = Blueprint('main', __name__)
photo = FileField('Profile picture', validators=[FileAllowed(img, 'Images only!')])


@main_bp.route('/')
def index():
    if not current_user.is_anonymous:
        name = current_user.first_name
        flash(f'Hello {name}. ')
    return render_template('index.html', title="Home")


@main_bp.route('/display_profiles', methods=['POST', 'GET'])
@main_bp.route('/display_profiles/<username>/', methods=['POST', 'GET'])
@login_required
def display_profiles(username=None):
    results = None
    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for("main.index"))
            results = Profile.query.filter(Profile.username.contains(term)).all()
    else:
        results = Profile.query.filter_by(username=username).all()
    if not results:
        flash("No users found.")
        return redirect(url_for("main.index"))
    # The following iterates through the results and adds the full url to a list of urls
    urls = []
    for result in results:
        url = img.url(
            result.photo)  # uses the global photos plus the photo file name to determine the full url path
        urls.append(url)
    return render_template('display_profile.html',
                           profiles=zip(results, urls))  # Note the zip to pass both lists as a parameter







