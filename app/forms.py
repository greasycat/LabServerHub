from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    email = StringField('Email Address', [validators.email()])
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('New Password', [validators.DataRequired()])
