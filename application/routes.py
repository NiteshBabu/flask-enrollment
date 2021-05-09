from flask.globals import request
from . import app
from .form import LoginForm, RegistrationForm
from flask import render_template, redirect, flash
import json
from .models import User

# creating routes
@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html', login=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm(request.form or None)
  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data

    user = User.objects(email=email).first()
    if user and user.password == (password):
      flash(f"{user.first_name}, Successfully Logged In !!", "success")
      return redirect('index')
    else:
      flash("Something Went Wrong !!", "danger")
  return render_template('login.html', title="login", form=form, login=True)


@app.route('/register', methods=["POST", "GET"])
def register():
  form = RegistrationForm(request.form or None)
  if form.validate_on_submit():
      flash("Created Account Successfully, Please Login !!", "success")

  return render_template('register.html', title="New User Registration", form=form, register=True)


@app.route('/courses/<string:term>/')
@app.route('/courses')
def courses(term=None):
  courseData = None
  with open('application/models/courses.json', 'r') as f:
    courseData = json.load(f)
  return render_template('courses.html', courseData=courseData, term=term.title(), courses=True)


@app.route('/enrollment', methods=['POST'])
def enrollment():
  # print(request.form.to_dict())

  # course_id = request.form.get('course_id')
  # title = request.form.get('title')
  # term = request.form.get('term')
  # data ={git 
  #   'course_id' : course_id,
  #   'title' : title,
  #   'term' : term,
  # }
  return render_template('enrollment.html', data={**request.form}, enrollment=True)
