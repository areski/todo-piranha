from wtforms import Form, BooleanField, StringField, validators
# from wtforms import HiddenField
from wtforms import PasswordField


class LoginForm(Form):
    login = StringField('Username', [validators.Length(min=4, max=40)])
    password = PasswordField('password', [validators.Length(min=4, max=40)])


class TaskForm(Form):
    taskname = StringField('Task', [validators.Length(min=2, max=255)])
    status = BooleanField('Status',
                          # [validators.InputRequired()],
                          default=True)
