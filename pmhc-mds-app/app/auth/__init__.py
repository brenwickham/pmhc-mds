from flask import Blueprint


bp = Blueprint('auth', __name__, template_folder='pages')

from app.auth import routes
