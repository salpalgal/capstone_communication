from flask import Flask,render_template,g,session,flash,redirect 
from flask_debugtoolbar import DebugToolbarExtension
import requests
import json
# from api_key import api_key
from forms import SignUpForm, LoginForm , SendEmailForm, EditProfileForm
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User
import os





app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///my_reads_db'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///communication_db'))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipe_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
CURR_USER_KEY = "curr_user"
connect_db(app)


db.create_all()


app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

debug = DebugToolbarExtension(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""
    # user = g.user
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route("/")
def root():
    return render_template("root.html", user=g.user)

@app.route("/home")
def home():
    if g.user:
        user = g.user
        users = User.query.all()
        return render_template("home.html", user = g.user, users=users)
    else:
        flash("please login","error")
        return redirect("/")

@app.route("/signup", methods = ["GET","POST"])
def signup():
    user = g.user
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                
            )
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/home")
    else:
        return render_template("signup.html", form = form)

@app.route("/login", methods =["GET","POST"])
def login():
    form = LoginForm()
    # user = g.user
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        
        if user:
            do_login(user)
            # flash(f"Hello, {user.username}!", "success")
            return redirect("/home")
        
    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    do_logout()
    if session.get('res') == True:
        session.pop("res")
    return redirect("/")

@app.route("/user/<int:user_id>")
def user_page(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    
    
    return render_template("user_page.html",user = user )
@app.route("/list")
def name_list():
    if g.user:
        user = g.user
        users = User.query.all()
        return render_template("list.html", user = g.user, users=users)
    else:
        flash("please login","error")
        return redirect("/")


@app.route("/user/<int:user_id>/email", methods = ["GET","POST"])
def profile_update(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id) 
    form = SendEmailForm()
    if form.validate_on_submit():
        send_to = form.send_to.data
        # send_from = form.send_From.data
        subject = form.subject.data
        content = form.content.data
        url = "https://api.us.nylas.com/send"
        payload = json.dumps({
        "body": content,
        "subject": subject,
        "to": [
        {
            "name": user.first_name,
            "email": send_to
        }
        ]
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': '[[Authorization-masked-secret]]'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        
        return redirect(f"/user/{user.id}") 
    else:
        return render_template("send_email.html", form = form, user = user)

    # @app.route("/search", methods = ["GET", "POST"])
# def search():
    
#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")
#     form = RecipeSearchForm()
#     if form.validate_on_submit():
#         ingredients = form.ingredients.data
#         number = form.number.data
#         res =  requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}",params={"ingredients": ingredients ,"number": number})
#         session["res"] = res.json()
    

#         return redirect(url_for('.search_list',res = res) )
#     else:
#         return render_template("search.html", form= form, user= g.user) 