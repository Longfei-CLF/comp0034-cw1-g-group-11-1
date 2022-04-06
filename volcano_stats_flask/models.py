from volcano_stats_flask import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class User(UserMixin,db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    profiles = db.relationship("Profile", uselist=False, backref=db.backref('user'))

    # def __repr__(self):
    #     return f"{self.id} {self.first_name} {self.last_name} {self.email} {self.password}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Profile (db.Model):
    __tablename__ = "Profile"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text, unique = True, nullable=False)
    photo = db.Column(db.Text)
    bio = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

class Organization (db.Model):
    __tablename__ = "organization"
    id = db.Column(db.Integer, primary_key = True)
    Organization = db.Column(db.Text)