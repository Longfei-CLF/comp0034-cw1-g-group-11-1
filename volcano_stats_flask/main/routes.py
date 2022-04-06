
from flask import Blueprint, render_template, flash
from flask_login import current_user

from flask_wtf.file import FileField, FileAllowed
from volcano_stats_flask.static import img
from flask_login import login_required
from flask import request, redirect, url_for

from volcano_stats_flask import photos, db
from volcano_stats_flask.main.forms import ProfileForm
from volcano_stats_flask.models import Profile, Organization
from volcano_stats_flask.models import User


main_bp = Blueprint('main', __name__)
photo = FileField('Profile picture', validators=[
                  FileAllowed(img, 'Images only!')])


@main_bp.route('/')
def index():
    if not current_user.is_anonymous:
        name = current_user.first_name
        flash(f'Hello {name}. ')
    return render_template('index.html', title="Home")


@main_bp.route('/community', methods=['GET', 'POST'])
@login_required
def community():
    results = Profile.query.all()
    photo_urls = []
    profile_urls = []
    for result in results:
        if result.photo:
            photo_url = photos.url(result.photo)
            photo_urls.append(photo_url)
            profile_url = "/display_profiles/" + result.username
            profile_urls.append(profile_url)
    return render_template('dispaly_community.html', profiles=zip(results, photo_urls, profile_urls))


@main_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    profile = Profile.query.join(User, User.id == Profile.user_id).filter(
        User.id == current_user.id).first()
    if profile:
        return redirect(url_for('main.display_profiles'))
    else:
        return redirect(url_for('main.create_profile'))


@main_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    form.organization_id.choices = [
        (r.id, r.organization) for r in Organization.query.order_by('organization')]
    if request.method == 'POST' and form.validate_on_submit():
        if 'photo' in request.form:
            if request.form['photo'].filename != '':
                filename = photos.save(request.form['photo'])
        p = Profile(organization_id=form.organization_id.data, username=form.username.data, photo=filename, bio=form.bio.data,
                    user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.display_profiles', username=p.username))
    return render_template('profile.html', form=form)


@main_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    profile = Profile.query.join(User, User.id == Profile.user_id).filter_by(
        id=current_user.id).first()

    form = ProfileForm(obj=profile)
    form.organization.choices = [(r.id, r.region)
                                 for r in Organization.query.order_by('org')]
    if request.method == 'POST' and form.validate_on_submit():
        if 'photo' in request.form:
            filename = photos.save(request.file['photo'])
            profile.photo = filename
        profile.region = form.org_id.data
        profile.bio = form.bio.data
        profile.username = form.username.data
        db.session.commit()
        return redirect(url_for('main.display_profiles', username=profile.username))
    return render_template('profile.html', form=form)


@main_bp.route('/display_profiles/<username>/', methods=['POST', 'GET'])
@main_bp.route('/display_profiles', methods=['POST', 'GET'], defaults={'username': None})
@login_required
def display_profiles(username):
    if username is None:
        results = Profile.query.filter_by(user_id=current_user.id).all()
    else:
        results = Profile.query.filter_by(username=username).all()
    if not results:
        flash("Username not found.")
        return redirect(url_for("main.index"))
    urls = []
    for result in results:
        if result.photo:
            url = photos.url(result.photo)
            urls.append(url)
    return render_template('display_profile.html', profiles=zip(results, urls))
