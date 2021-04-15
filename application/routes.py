from . import app
from flask import render_template


# creating routes
@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/login')
def login():
  return render_template('login.html')


@app.route('/register')
def register():
  return render_template('register.html')


@app.route('/classes')
def classes():
  return render_template('courses.html')