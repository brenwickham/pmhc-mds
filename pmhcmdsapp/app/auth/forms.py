import operator
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import validators, HiddenField, StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length
# from app.models import User, Organisation


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()], render_kw={"autofocus": True, "required": True})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"required": True})
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign in")

class ChangePasswordForm(FlaskForm):
    userid = HiddenField()
    password = PasswordField('Password', validators=[InputRequired()])
    confirmpassword = PasswordField('Confirm password', validators=[InputRequired()])
    savepassword = SubmitField("Save password")


class ProfileForm(FlaskForm):
    firstname = StringField("First name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    email = StringField("Email", [validators.InputRequired()])
    current_organisation_id = SelectField(u"Current organisation", coerce=int)
    submit = SubmitField("Save profile")

    def validate(self):

        if not FlaskForm.validate(self):
            return False
        result = True
        return result


class UserAccountForm(FlaskForm):
    id = HiddenField()
    firstname = StringField(u'First name', validators=[InputRequired()])
    surname = StringField(u'Last name', validators=[InputRequired()])
    email = StringField(u'Email', validators=[InputRequired()])
    current_organisation_id = SelectField(u'Current organisation', coerce=int)
    isactive = SelectField(u'Status', coerce=int)
    passwordexpired = BooleanField(u'Password expired')
    saveaccount = SubmitField('Save account')

    def validate(self, user):
        organisations = [(0,"---")]
        if user:
            organisations += [(p.organisation_id, p.organisation.name) for p in user.organisations]
            organisations.sort(key=operator.itemgetter(1))
        self.current_organisation_id.choices = organisations
        self.isactive.choices = [(1, "Active"), (0, "Inactive")]
        if not FlaskForm.validate(self):
            return False
        result = True
        return result
