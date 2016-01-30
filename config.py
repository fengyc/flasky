import os
import hashlib

basedir = os.path.abspath((os.path.dirname(__file__)))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                 hashlib.sha256('TOP_SECRET'.encode()).hexdigest()
    # sqlalchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.ym.163.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT')) if os.environ.get('MAIL_PORT') else 465
    MAIL_USE_SSL = str(True) == os.environ.get('MAIL_USE_SSL') if os.environ.get('MAIL_USE_SSL') else True
    MAIL_USE_TLS = str(True) == os.environ.get('MAIL_USE_TLS') if os.environ.get('MAIL_USE_TLS') else False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER') or MAIL_USERNAME
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                             'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                             'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                             'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'product': ProductConfig,

    'default': DevelopmentConfig,
}