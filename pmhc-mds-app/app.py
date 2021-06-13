#!flask/bin/python

from app import create_app#, db
# from app.models import User
from config import Config

application = create_app()

# @application.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User}

if __name__ == "__main__":
    #Use , host="0.0.0.0" for testing mobile device on local dev machine.
    application.run(debug=Config.DEBUG,ssl_context=Config.SSL_CONTEXT )
