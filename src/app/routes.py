from app import app, db
from app.models import User, Order, Product, Item
from app.forms import SignUpForm, LoginForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt
from .forms import OrderForm

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

#==========================LOGIN/SIGNOUT=========================#

@app.route ('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user_id = form.id.data
            user = User.query.filter_by(id=user_id).first()

            print("Form data - ID:", user_id)  # Debug statement
            print("User found:", user)  # Debug statement

            if user:
                if bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
                    print("Password matched")
                    login_user(user)
                    print("Redirecting to products...")
                    return redirect(url_for('products'))  # Redirect to products page
                else:
                    print("Password mismatch")
            else:
                print("User not found for ID:", user_id)

        except Exception as e:
            print("Error occurred during login:", e)



    '''if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd): #check for matching PW
            print("Login successful!")  # Debug message
            login_user(user)
            print("Redirecting to place_order...")  # Debug message
            return redirect(url_for('place_order'))
        else:
            print("Login failed!")  # Debug message'''

   

    return render_template('login.html', form=form)

@app.route('/signout', methods=['GET', 'POST'])
def signout():

    logout_user()

    return redirect(url_for('index'))

#================================================================#

#==========================SIGNUP================================#

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print("Form submitted successfully")  # Print a message when the form is submitted
        if form.passwd.data == form.passwd_confirm.data:
            hashed = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())

            # Create User
            user = User(
                id=form.id.data,
                name=form.name.data, 
                passwd=hashed,
                creation_date=form.creation_date.data
            )

            # Store in DB
            db.session.add(user)
            db.session.commit()
            print("User added to the database")  # Print a message when the user is added to the database
            return redirect(url_for('login'))
        else:
            print("Password confirmation does not match")  # Print a message if password confirmation does not match
    else:
        print("Form validation failed")  # Print a message if form validation fails
        print(form.errors)

    return render_template('signup.html', form=form)


#================================================================#

#==========================PRODUCTS==============================#

@app.route('/products', methods=['GET', 'POST'])
@login_required
def place_order():
    form = OrderForm()
    if form.validate_on_submit():
        #process into DB
        order_number = form.number.data
        creation_date = form.creation_date.data
        status = form.status.data
        items = form.items.data

        #Debug test print of form data
        print(f"Order Number: {order_number}")
        print(f"Creation Date: {creation_date}")
        print(f"Status: {status}")
        for item in items:
            print(f"Item: {item}")

        return redirect(url_for('place_order'))
    return render_template('products.html', form=form)

@app.route('/place_order') 
def order_placed():
    return "Order Placed Successfully"




#================================================================#