import os
import base64
from datetime import datetime, timedelta
from operator import attrgetter, itemgetter
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import sqlalchemy as sa
from sqlalchemy_continuum.plugins import FlaskPlugin
from sqlalchemy_continuum import make_versioned
# from app import db, login


#This line critical, it's required for sqlalchemy_continuum versioning:
make_versioned(plugins=[FlaskPlugin()])

#Extending a class from this class enables get_dict automatically, returning column names and field values:
class BaseModel(object):

    @classmethod
    def _get_keys(cls):
        return db.class_mapper(cls).c.keys()
    
    def get_dict(self):
        d = {}
        for k in self._get_keys():
            d[k] = getattr(self, k)
        return d

#Suggestion to use, and explaination of, CRUDMixin comes from https://realpython.com/python-web-applications-with-flask-part-ii/
#Customisations from original CRUDMixin:
# - create method removes the id field from the dict (otherwise it will error because value passed through is 'None').
# - added fill_with_formdata method (so it's easy to pass the class back to a form that failed validation).
class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any(
            (
                isinstance(id, str) and id.isdigit(),
                isinstance(id, (int, float))
            ),
        ):
            return cls.query.get(int(id))
        return None

    @classmethod
    def create(cls, **kwargs):
        classdict = {k: v for k, v in kwargs.items() if k in cls._get_keys()}
        instance = cls(**classdict)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    @classmethod
    def fill_with_formdata(cls, formdata):
        classdict = {k: v for k, v in formdata.items() if k in cls._get_keys()}
        return cls(**classdict)


class User(BaseModel, UserMixin, db.Model):
    __tablename__ = 'user'
    __versioned__ = {}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), index=True, unique=True)
    firstname = db.Column(db.String(64), index=True, )
    surname = db.Column(db.String(64), index=True, )
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean ,default=False)
    is_active = db.Column(db.Boolean, default=True)
    passwordexpired = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
#    roles = db.relationship("UserRole")
#    currentorganisation_id = db.Column(db.Integer, db.ForeignKey("organisation.id"), index=True)
#    currentorganisation = db.relationship("app.models.Organisation", backref=db.backref("currentorganisation"))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
        
    def rolelist(self):
        return [r.role_id for r in self.roles]

    def can_delete(self):
        #If user is in  Admin (2) role, then they can delete:
        if set(self.rolelist()).intersection(set([2])):
            return True
        else:
            return False

    def to_dict(self):
        teams = []
        if self.teams:
            teams = sorted([{"organisation_id": t.organisation.id, "team":t.organisation.organisation_name, "user_id": self.id} for t in self.teams], key=itemgetter('team'))
        return {
            "id":self.id,
            "email": self.email,
            "firstname":self.firstname,
            "surname": self.surname,
            "isadmin":self.isadmin,
            "isactive":self.isactive,
            "passwordexpired": self.passwordexpired,
            "haspassword": False if not self.password_hash else True,
            "roles": [{"role_id": r.role.id, "role":r.role.rolename, "user_id": self.id} for r in self.roles],
            "teams": teams
        }

@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class Announcement(BaseModel, db.Model):
    __tablename__ = 'announcement'
    __versioned__ = {}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(120))
    announcement = db.Column(db.Text())
    announcementdate = db.Column(db.Date)
    type = db.Column(db.Integer,default=1)
    status = db.Column(db.Integer,default=1)


class Role(BaseModel, db.Model):
    __tablename__ = 'role'
    __versioned__ = {}

    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(120))


class UserRole(db.Model):
    __versioned__ = {}

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id), primary_key=True)
#    role = db.relationship(Role, backref=db.backref("role_assoc"))
#    user = db.relationship(User, backref=db.backref("user_assoc"))


class UserOrganisation(BaseModel, db.Model):
    __tablename__ = 'user_organisation'
    __versioned__ = {}

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey("organisation.id"), primary_key=True)
#    user = db.relationship("app.models.User", backref=db.backref("user2_assoc"))
#    organisation = db.relationship("app.models.Organisation", backref=db.backref("userorg_assoc"))


class Organisation(BaseModel, db.Model, CRUDMixin):
    __tablename__ = 'organisation'
    __versioned__ = {}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.SmallInteger)
#    users = db.relationship(UserOrganisation, backref=db.backref("users"))

    
    

    

#Lookups:
# class lkup_example(BaseModel, db.Model):
#     id = db.Column(db.SmallInteger, primary_key=True, autoincrement=False)
#     example = db.Column(db.String(150))




#This line critical. It configures the sqlalchemy_continuum versioning:
sa.orm.configure_mappers()
