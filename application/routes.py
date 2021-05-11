from flask.globals import request
from flask.helpers import url_for
from . import app
from .form import LoginForm, NewCourseForm, RegistrationForm
from flask import render_template, redirect, flash, session
import json
from .models import Enrollment, User, Course


# creating routes
@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

  if session["user_id"]:
    return redirect(url_for('index'))

  form = LoginForm(request.form or None)
  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data

    user = User.objects(email=email).first()
    if user and user.get_password(password):
      session["user_id"] = user.user_id
      session["username"] = user.first_name
      flash(f"Welcome {user.first_name}, Successfully Logged In !!", "success")
      return redirect(url_for("index"))
    else:
      flash("Something Went Wrong !!", "danger")
  return render_template('login.html', title="login", form=form, login=True)


@app.route("/logout")
def logout():
  if not session["user_id"]:
    flash("Please Login to Continue !!", "danger")
    return redirect(url_for("login"))

  session["user_id"] = False
  session.pop("username", None)
  
  flash("Succesfully Logged Out !!", "success")
  return redirect(url_for('index'))


@app.route('/register', methods=["POST", "GET"])
def register():
 
  if session["user_id"]:
    return redirect(url_for('index'))
 
  form = RegistrationForm(request.form or None)
  if form.validate_on_submit():
    user_id = User.objects.count() + 1
    password = form.password.data
    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data

    user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()
    flash("Created Account Successfully, Please Login !!", "success")
    return redirect(url_for('login'))
  return render_template('register.html', title="New User Registration", form=form, register=True)


@app.route('/courses/<string:term>/')
@app.route('/courses')
def courses(term=None):
  print(session["user_id"])
  courseData = Course.objects.all().order_by('-course_id')
  # with open('application/models/courses.json', 'r') as f:
  #   courseData = json.load(f)
  return render_template('courses.html', courseData=courseData, term=term and term.title(), courses=True)


@app.route('/courses/new', methods=['GET', 'POST'])
def new_course():
  form = NewCourseForm(request.form or None)
  if form.validate_on_submit():
    Course.objects.create(course_id=form.course_id.data, title=form.title.data,description= form.description.data,credits= form.credits.data,term= form.term.data)
    return redirect(url_for('courses'))
  return render_template('new_course.html',title="New Course", form=form)


@app.route('/enrollment', methods=['POST', 'GET'])
def enrollment():
  if not session["user_id"]:
    flash("Please Login to Continue !!", "danger")
    return redirect(url_for("login"))

  user_id = session["user_id"]

  if request.method == 'POST':
    course_id = request.form["course_id"]
    course_title = request.form["title"]
    if Enrollment.objects(user=user_id, course=course_id):
      flash(f"You're already enrolled in {course_title} !!", "danger")
      return redirect(url_for('courses'))
    else:
      Enrollment(course=course_id, user=user_id).save()
      flash(f"You're successfully enrolled in {course_title} !!", "success")

  enrollments = Enrollment.objects.filter(user=user_id)
  classes = []
  for e in enrollments:
    classes.append(Course.objects.get(course_id = e.course))
  # print(request.form.to_dict())
  # course_id = request.form.get('course_id')
  # title = request.form.get('title')
  # term = request.form.get('term')
  # data ={
  #   'course_id' : course_id,
  #   'title' : title,
  #   'term' : term,
  # }
  # return render_template('enrollment.html', data={**request.form}, enrollment=True)

  return render_template('enrollment.html', classes=classes, enrollment=True)


