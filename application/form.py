from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .models import User


class LoginForm(FlaskForm):
  email = StringField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
  remember_me = BooleanField("Remember Me")
  submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
  email = StringField("Email", validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[
                            DataRequired(), Length(min=6, max=15)])
  confirm_password = PasswordField("Confirm Password", validators=[
                            DataRequired(), Length(min=6, max=15), EqualTo('password')])
  first_name = StringField("First Name", validators=[DataRequired()])
  last_name = StringField("Last Name", validators=[DataRequired()])
  submit = SubmitField("Register")

  def validate_email(self, email):
    if User.objects(email=email.data):
      raise ValidationError('Email already in use, Try other one !!')
