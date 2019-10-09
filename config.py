import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'top-secret'
    JWT_ACCESS_LIFESPAN = {'hours': 24}
    JWT_REFRESH_LIFESPAN = {'days': 30}
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    PRAETORIAN_CONFIRMATION_SENDER = os.environ.get('MAIL_USERNAME')
    PRAETORIAN_CONFIRMATION_URI = 'http://localhost:5000/api/v1/verify'
    FLASKY_MAIL_SUBJECT_PREFIX = "User Registration"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SLOW_DB_QUERY_TIME=0.5
    SSL_REDIRECT = False
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
         'sqlite:///' + os.path.join(basedir, 'app.db')



config = {
	'development': DevelopmentConfig,
	'default': DevelopmentConfig
}