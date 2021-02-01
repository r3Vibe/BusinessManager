from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash

# login form


class Login(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={
                           "placeholder": "Enter Your Username"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={
                             "placeholder": "Enter Your Password"})
    submit = SubmitField("Login")
