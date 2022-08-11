from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired, URL, NumberRange

class CreateUserForm(FlaskForm):
    """Form for creating a user"""

    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=20)])

    password = PasswordField('Password', [validators.DataRequired()])
    
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=50)])
    first_name = StringField('First Name', [validators.DataRequired(), validators.Length(min=3, max=30)])
    last_name = StringField('Last Name', [validators.DataRequired(), validators.Length(min=3, max=30)])

class LoginForm(FlaskForm):
    """Form for logging in a user"""

    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=20)])

    password = PasswordField('Password', [validators.DataRequired()])

class CreateFeedback(FlaskForm):
    """Form for creating a user"""

    title = StringField('Title', [validators.DataRequired(), validators.Length(min=4, max=100)])
    content = StringField('Content', [validators.DataRequired()])