from . import app
from flask import render_template
import json

# creating routes
@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html', login=True)

@app.route('/login')
def login():
  return render_template('login.html')


@app.route('/register')
def register():
  return render_template('register.html')


@app.route('/courses')
def courses():
  courseData = None
  term = 6
  with open('application/models/courses.json', 'r') as f:
    courseData = json.load(f)
  return render_template('courses.html', courseData=courseData, term=term)


@app.route('/enrollment')
def enrollment():
  return render_template('enrollment.html')