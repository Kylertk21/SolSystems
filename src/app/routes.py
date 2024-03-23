from app import app, db
from app.models import User, Order, Product, Item
from app.forms import SignUpForm, LoginForm, AdminForm, OrderStatusForm, ProductUpdateForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt
from .forms import OrderForm, ProductForm
from sqlalchemy.dialects.postgresql import insert

ADMIN_IDS = ['tmota']

def admin():
    return current_user.id in ADMIN_IDS if current_user.is_authenticated else False 

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

#==========================LOGIN/SIGNOUT=========================#

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user_id = form.id.data
            user = User.query.filter_by(id=user_id).first()

            if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
                login_user(user)
                if admin():
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('products'))
            else:
                print("User not found or password mismatch")
        except Exception as e:
            print("Error occurred during login:", e)

    return render_template('login.html', form=form)

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('index'))

#================================================================#

#==========================ADMIN DASHBOARD=========================#



@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not admin():
        return "Admin Access Only"
    
    order_status_form = OrderStatusForm()
    product_update_form = ProductUpdateForm()

    if order_status_form.validate_on_submit():
        # Logic to change order status
        order_id = order_status_form.order_id.data
        new_status = order_status_form.status.data
        # Update order status in the database
        # Redirect or render a template

    if product_update_form.validate_on_submit():
        # Logic to update product catalog
        code = product_update_form.code.data
        description = product_update_form.description.data
        availability = product_update_form.availability.data
        price = product_update_form.price.data
        # Update product in the database
        # Redirect or render a template

    return render_template('admin.html', order_status_form=order_status_form, product_update_form=product_update_form)



#================================================================#

#==========================SIGNUP================================#

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(id=form.id.data).first()
        if existing_user:
            return redirect(url_for('login'))
        if form.passwd.data == form.passwd_confirm.data:
            hashed = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())
            is_admin = form.id.data in ADMIN_IDS

            # Create User
            user = User(
                id=form.id.data,
                name=form.name.data, 
                passwd=hashed,
                creation_date=form.creation_date.data,
                role=is_admin
            )

            # Store in DB
            db.session.add(user)
            db.session.commit()
            print("User added to the database")
            return redirect(url_for('login'))
        else:
            print("Password confirmation does not match")
    else:
        print("Form validation failed")
        print(form.errors)

    return render_template('signup.html', form=form)

#================================================================#

#==========================Place Order==============================#

@app.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            number=form.number.data,
            creation_date=form.creation_date.data,
            status=form.status.data,
        )
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('order_placed'))
    return render_template('place_order.html', form=form)

@app.route('/order_placed') 
def order_placed():
    return "Order Placed Successfully"

#================================================================#

#==========================Products==============================#

@app.route('/products', methods=['GET'])
@login_required
def products():
    products = Product.query.all() 
    return render_template('products.html', products=products)

#================================================================#

