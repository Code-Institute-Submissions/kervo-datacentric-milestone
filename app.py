import os
from flask import Flask, app, redirect, render_template, request, url_for
from register import signUpForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.form import FlaskForm
from flask_pymongo import PyMongo
from forms import *
from flask.helpers import flash
from virtualenv import session

from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# Variables for database
mongo = PyMongo(app)
users_files = mongo.db.usersfiles

@app.route('/')
def index():
    return render_template("index.html", title='Wondercook')

@app.route('/login')
def login():
    return render_template("login.html", title='Log In')

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/signup')
def signup():
   if users_files in session:
        flash('This user is already registered')
        return redirect(url_for('/'))
        form = signUpForm()
        if form.validate_on_submit():
            users = users_files
            registered_user = users_files.find_one({'username': request.form['username']})

        if registered_user:
            flash("This user name already exists")
            return redirect(url_for('signup'))
        
        else:
            encrypted_password = generate_password_hash(request.form['password'])
            new_user = {
                "username": request.form['username'],
                "password": encrypted_password,
                "recipes": [],
            }
            users.insert_one(new_user)
            session["username"] = request.form['username']
            flash("You are ready to use wondercook")
            return redirect(url_for('dashboard'))
        
        return render_template('signup.html', form=form, title='Sign Up')


@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run()