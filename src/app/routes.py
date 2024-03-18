from app import app, db, load_user
from app.models import User, Recipe
from app.forms import SignUpForm, LoginForm, RecipeForm
from flask import render_template, reditect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

#==========================LOGIN/SIGNOUT=========================#
#================================================================#

#==========================SIGNUP================================#
#================================================================#

#==========================PRODUCTS==============================#
#================================================================#