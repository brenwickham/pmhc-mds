import os
import operator
import ast
from datetime import datetime
import json
from flask import Flask
from flask import render_template, abort, flash, redirect, url_for, request, send_file, current_app, send_from_directory
from flask_login import current_user, login_required
from flask.json import jsonify
from sqlalchemy import func, and_, or_, desc
from sqlalchemy.sql import label
# from app import db
from app.util import filters
from app.auth.forms import ProfileForm, ChangePasswordForm
# from app.models import User, UserRole, Role, Announcement
from app.main import bp


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html", title="Home")


#Generate favicons from https://favicon.io/favicon-converter/
@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static/img'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/apple-touch-icon.png')
def apple_touch_icon():
    return send_from_directory(os.path.join(current_app.root_path, 'static/img'), 'apple-touch-icon.png')

@bp.route('/favicon-32x32.png')
def favicon_32x32():
    return send_from_directory(os.path.join(current_app.root_path, 'static/img'), 'favicon-32x32.png')

@bp.route('/favicon-16x16.png')
def favicon_16x16():
    return send_from_directory(os.path.join(current_app.root_path, 'static/img'), 'favicon-16x16.png')

@bp.route('/site.webmanifest')
def site_webmanifest():
    return send_from_directory(os.path.join(current_app.root_path, 'static/img'), 'site.webmanifest')





#Tips:
# 
# Detect if a checkbox value (example shows a field called "is_removed") is off if user doesn't explicitly change it (otherwise it will be marked as on):
# if request.form.get('is_removed') == '':
#    myform.is_removed.data = True
#






