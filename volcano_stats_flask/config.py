"""Flask config class."""


from asyncio import FastChildWatcher
from distutils.debug import DEBUG
from pathlib import Path
import pathlib
import os

from django.views.generic import View


# class Config():

#     CSRF_ENABLED = True
#     SECRET_KEY = 'YOU-WILL-SUCCEED'


#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flaskblog?charset=utf8'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     POSTS_PRE_PAGE = 3

#Code for sending the email to user, however the function can not run properly.
    # MAIL_SUPPRESS_SEND = False  #
    # MAIL_SERVER = 'smtp.sina.cn'
    # MAIL_PORT = int(465)
    # MAIL_USE_SSL = True
    # MAIL_PASSWORD = 'xxxxx'
    # MAIL_USERNAME = 'xx'
    # ADMINS = ['xxxxxx@outlook.cn']


class Config(object):
    DEBUG = False
    SECRET_KEY = 'b0m2sjek18Ta5-r8Px9tvA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_PATH = pathlib.Path(__file__).parent
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(DATA_PATH.joinpath('flask_db.sqlite'))
    UPLOADED_PHOTOS_DEST = Path(__file__).parent.joinpath("static/img")


class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    ENV = 'testing'
    DEBUG = False


