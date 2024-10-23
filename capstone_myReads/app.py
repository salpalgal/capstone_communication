from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
import requests
# from api_key import api_key
# from forms import SignUpForm, LoginForm , RecipeSearchForm, EditProfileForm
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///my_reads_db'))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipe_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

db.create_all()


@app.route("/")
def root():
    return render_template("home.html")



