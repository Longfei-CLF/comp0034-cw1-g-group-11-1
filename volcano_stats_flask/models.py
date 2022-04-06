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

    def __repr__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.email} {self.password}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Profile (db.Model):
    __tablename__ = "Profile"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text, unique = True)
    photo = db.Column(db.Text)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
          return '<User %r>' % (self.nickname)


# The jwt can form a token, however the email can not be sent.
# import jwt
#
# class User(UserMixin, db.Model):
#         ......
#
#     def get_jwt_token(self, expires_in=600):
#         """
#         get jwt token
#         """
#         return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
#                           current_app.config['SECRET_KEY'],
#                           algorithm='HS256').decode('utf8')
#
#     @staticmethod
#     def verify_jwt_token(token):
#         try:
#             user_id = jwt.decode(token,
#                                  current_app.config['SECRET_KEY'],
#                                  algorithms='HS256')['reset_password']
#         except Exception as e:
#             print(e)
#             return
#         return User.query.get(user_id)
#
#     def __repr__(self):
#
#         return '<User %r>' % self.username
