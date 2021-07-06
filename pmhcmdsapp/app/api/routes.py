from datetime import datetime, time, date
from sqlalchemy import func, or_
from flask_login import current_user
from flask import jsonify, g, request, abort
from app import Config
# from app import db
from app.api import bp
from app.api.auth import token_auth
# from app.models import User, UserRole, Role, Organisation, UserOrganisation

currentrecord = ""

class APIError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv



@bp.errorhandler(APIError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@bp.route('/health', methods=['GET','POST'])
def health():
    return 'OK'




#How to access endpoints:

# The code for the API looks for 'data' in the json payload. Examples:
# In httpie it looks like this: http GET http://localhost:5000/api/download "Authorization:Bearer TOKENSUPPLIEDBYAPIAUTHENTICATION" data:='{"datefrom": "2019-10-01" }'
# Python request code ("data" is there solely to work with httpie):
# r = requests.post(root_url + '/api/download', headers={'Authorization': 'Bearer {}'.format(token)},json={"data": {"datefrom": "2019-10-15", "dateto": "2019-11-30"}})

#Using httpie:
#This returns a token:
#http --auth dev@test.com:writeyourpasswordhere POST http://localhost:5000/api/tokens
#Use the returned token:
#http GET http://localhost:5000/api/download 'Authorization:Bearer writeintokenhere'
#Delete token:
#http DELETE http://localhost:5000/api/tokens Authorization:'Bearer writeintokenhere'

#Using python requests module:
#r = requests.post(root_url + '/api/tokens', auth=HTTPBasicAuth(writeyouremailhere, writeyourpasswordhere))
#token = r.json()['token']
#r = requests.post(root_url + '/api/download', headers={'Authorization': 'Bearer {}'.format(token)})
#data = r.json()


