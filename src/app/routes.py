from app import app
from flask import render_template, redirect, url_for
from app.forms import SignInForm, SignUpForm
from datetime import datetime
from flask_login import login_required, login_user, logout_user, current_user
from app.models import *
from app.forms import *
from app import db
from flask import flash

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    form = SignInForm()
    if form.validate_on_submit(): 
        return redirect(url_for('orders'))
    else:
        return render_template('users_signin.html', form=form)

@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    form = SignUpForm()
    if form.validate_on_submit(): 
        return redirect(url_for('index'))
    else:
        return render_template('users_signup.html', form=form)  
      
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user
    return redirect(url_for('index'))


products = [
        { 
            'code': 101, 
            'description': '6x8 monocrystalline cell panel, 240W', 
            'available': True, 
            'price': 150.00
        }, 
        { 
            'code': 202, 
            'description': '6x10 monocrystalline cell panel, 310W', 
            'available': True, 
            'price': 300.00
        },
        { 
            'code': 303, 
            'description': '6x12 monocrystalline cell panel, 400W', 
            'available': True, 
            'price': 450.00
        }
    ]


@app.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    form = OrderForm()
    if form.validate_on_submit():
        # Create a new order object with the submitted data
        order = Order(user_id=current_user.id, product_id=form.product.data, quantity=form.quantity.data)
        
        # Add the order to the database session
        db.session.add(order)
        db.session.commit()
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('place_order.html', form=form)

@app.route('/orders')
@login_required
def orders():
    orders = current_user.orders.all()
    return render_template('orders.html', orders=orders)

@app.route('/admin/products', methods=['GET', 'POST'])
@login_required
def admin_products():
    form = ProductForm()
    if form.validate_on_submit():
        # Create a new product object with the submitted data
        product = Product(code=form.code.data, description=form.description.data, price=form.price.data)
        
        # Add the product to the database session
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    products = Product.query.all()
    return render_template('admin_products.html', form=form, products=products)

@app.route('/admin/orders')
@login_required
def admin_orders():
    orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders)
