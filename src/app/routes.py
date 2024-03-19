from app import app, db
from app.models import User, Order, Product, Item
from app.forms import SignUpForm, LoginForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

#==========================LOGIN/SIGNOUT=========================#
@app.route ('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()

        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd): #check for matching PW
            login_user(user)
            return redirect(url_for('products'))

#================================================================#

#==========================SIGNUP================================#
#================================================================#

#==========================PRODUCTS==============================#
#================================================================#