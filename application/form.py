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
    if User.objects(email=email.data).first():
      raise ValidationError('Email already in use, Try other one !!')


class NewCourseForm(FlaskForm):
  course_id = StringField("Course ID", validators=[DataRequired(), Length(min=4, max=10)])
  title = StringField("Title", validators=[DataRequired(), Length(min=2, max=10)])
  description = StringField("Description", validators=[DataRequired(), Length(min=10, max=100)])
  credits = StringField("Credits", validators=[DataRequired()])
  term = StringField("Term", validators=[DataRequired(), Length(min=3, max=10)])
  submit = SubmitField("Submit")