from app import app, db
from app.models import User, Order, Product, Item
from app.forms import SignUpForm, LoginForm, AdminForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt
from .forms import OrderForm, ProductForm
from sqlalchemy.dialects.postgresql import insert
from flask import flash

ADMIN_IDS = ['tmota']

def admin():
    return current_user.is_authenticated and current_user.id in ADMIN_IDS
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
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('user_dashboard'))
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
    if admin():
        # Pass an empty form to the template
        form = AdminForm()  # Replace SomeForm with the appropriate form class
        return render_template('admin.html', form=form)
    else:
        return "Admin Access Only"


#================================================================#

#==========================SIGNUP================================#

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(id=form.id.data).first()
        if existing_user:
            return redirect(url_for('index'))
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
            flash('Signed up successfully!', 'success')
            return redirect(url_for('index'))
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
    # Create an instance of the OrderForm
    form = OrderForm()

    # Fetch available products from the database or use the provided list
    products = [
        {'code': 101, 'description': '6x8 monocrystalline cell panel, 240W', 'price': 150.00},
        {'code': 202, 'description': '6x10 monocrystalline cell panel, 310W', 'price': 300.00},
        {'code': 303, 'description': '6x12 monocrystalline cell panel, 400W', 'price': 450.00}
    ]

    # Populate the products field of the form with the available products
    form.products.entries = [
        ProductForm(code=product['code'], description=product['description'], price=product['price']) 
        for product in products
    ]

    if form.validate_on_submit():
        # Process the form data and create the order
        order = Order(
            number=form.number.data,
            creation_date=form.creation_date.data,
            status=form.status.data,
            user_id=current_user.id
        )

        # Add items to the order based on the form data
        for product_form in form.products.entries:
            # Create an Item object and add it to the order
            item = Product(
                code=product_form.code.data,
                description=product_form.description.data,
                price=product_form.price.data
            )
            order.products.append(item)

        # Save the order to the database
        db.session.add(order)
        db.session.commit()

        # Redirect to the order placed confirmation page
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

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/track_orders', methods=['GET'])
@login_required  # Ensure the user is authenticated
def track_orders():
    try:
        # Query the database for orders associated with the current user
        orders = Order.query.filter_by(customer_id=current_user.id).all()

        # Prepare a list of order data to pass to the template
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'product_id': order.product_id,
                'status': order.status,
            })

        # Render the track orders template and pass the orders data
        return render_template('track_orders.html', orders=orders_data)
    except Exception as e:
        flash("Error occurred while tracking orders: " + str(e), 'error')
        return redirect(url_for('user_dashboard'))

