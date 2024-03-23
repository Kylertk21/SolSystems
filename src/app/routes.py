from app import app, db
from app.models import User, Order, Product, Item
from app.forms import SignUpForm, LoginForm, AdminForm, OrderStatusForm, ProductUpdateForm, OrderForm, ProductForm
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

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
                    return redirect(url_for('user_dashboard'))
            else:
                flash("User not found or password mismatch", 'error')
        except Exception as e:
            flash("Error occurred during login: " + str(e), 'error')

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
            flash("User already exists. Please login.", 'error')
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
            flash('Signed up successfully!', 'success')
            return redirect(url_for('login'))
        else:
            flash("Password confirmation does not match", 'error')
    else:
        flash("Form validation failed", 'error')
        flash(form.errors, 'error')

    return render_template('signup.html', form=form)

#================================================================#

#==========================Place Order==============================#

@app.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    form = OrderForm()

    products = [
        {'code': 101, 'description': '6x8 monocrystalline cell panel, 240W', 'price': 150.00},
        {'code': 202, 'description': '6x10 monocrystalline cell panel, 310W', 'price': 300.00},
        {'code': 303, 'description': '6x12 monocrystalline cell panel, 400W', 'price': 450.00}
    ]

    for product_data in products:
        existing_product = Product.query.filter_by(code=product_data['code']).first()
        if existing_product:
            # Product already exists, handle update or skip
            pass
        else:
            # Insert the new product
            new_product = Product(
                code=product_data['code'],
                description=product_data['description'],
                price=product_data['price']
            )
            db.session.add(new_product)

    # Commit changes to the database
    db.session.commit()

    if form.validate_on_submit():
        order = Order(
            number=form.number.data,
            creation_date=form.creation_date.data,
            status=form.status.data,
            user_id=current_user.id
        )

        # Save the order to the database
        db.session.add(order)
        db.session.commit()

        flash('Order placed successfully!', 'success')
        return redirect(url_for('order_placed'))

    # If form is not submitted or validation fails, render the form
    return render_template('place_order.html', form=form, products=products)

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

