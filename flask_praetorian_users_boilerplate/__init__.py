import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_praetorian import Praetorian
from flask_mail import Mail
from config import config


db = SQLAlchemy()
cors = CORS()
guard = Praetorian()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    
    from .models.user import User
    guard.init_app(app, User)


    from .blueprints.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app