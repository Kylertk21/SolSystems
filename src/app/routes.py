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
        
    return render_template('login.html', form=form)

@app.route('/users/signout', methods=['GET', 'POST'])
def signout():

    logout_user()

    return redirect(url_for('index'))

#================================================================#

#==========================SIGNUP================================#

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.passwd.data == form.passwd_confirm.data:
            password = b"password"  #hash PW

        hashed = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcypt.gensalt())

        #Create User
        user = User(
            id=form.id.data,
            name=form.name.data, 
            passwd=hashed,
            c_date=form.creation_date.data
        )

        #Store in DB
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('signup.html', form=form)

#================================================================#

#==========================PRODUCTS==============================#






#================================================================#