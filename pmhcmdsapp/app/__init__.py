import os
from datetime import datetime
from flask import Flask, render_template, request
from config import Config
import logging
from logging.handlers import RotatingFileHandler
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


def bad_request(e):
    if request.is_xhr: #Response if AJAX request
        return e, 400
    else:
        return render_template('400.html',errordatetime=datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S"), error=e, requestpath=request.path), 400

def file_too_large(e):
    return render_template('413.html'), 413

def page_not_found(e):
    return render_template('404.html'), 404

def system_error(e):
    if request.is_xhr: #Response if AJAX request
        return e, 500
    else:
        return render_template('500.html',errordatetime=datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S"), error=e), 500
        
        
#This is used to set the convention for naming db entities (e.g. keys and indexes). Useful for migrating and downgrading smoothly).
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
# db = SQLAlchemy(metadata=metadata)
# migrate = Migrate()

login = LoginManager()
# login.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # db.init_app(app)
    # migrate.init_app(app, db)
    login.init_app(app)

    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(413, file_too_large)
    app.register_error_handler(500, system_error)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        #Set up log file:
        file_handler = RotatingFileHandler(Config.LOGFOLDER + "pmhc-mds.log", "a", 1 * 1024 * 1024, 10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    csrf = CSRFProtect(app)    
    csrf.exempt(api_bp)
    return app

#Any app import statements MUST be placed after the create_app method,
#otherwise you will get a NameEror ("...is not defined"):
from app.util import filters
from app import models
