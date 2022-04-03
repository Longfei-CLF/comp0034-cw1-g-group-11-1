"""Flask config class."""


from asyncio import FastChildWatcher
from distutils.debug import DEBUG
from pathlib import Path
import pathlib


class Config(object):
    DEBUG = False
    SECRET_KEY = 'b0m2sjek18Ta5-r8Px9tvA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_PATH = pathlib.Path(__file__).parent
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(DATA_PATH.joinpath('flask_db.sqlite'))
    UPLOADED_PHOTOS_DEST = Path(__file__).parent.joinpath("volcano_stats_flask/static/img")


class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    ENV = 'testing'
    DEBUG = False
