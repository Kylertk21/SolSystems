from app import app, db
from app.models import User, Order, Product, Item
from app.forms import SignUpForm, LoginForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt
from .forms import OrderForm, ProductForm
from sqlalchemy.dialects.postgresql import insert

ADMIN_IDS = ['tmota']

def admin():
    return current_user.is_admin in ADMIN_IDS if current_user.is_authenticated else False 

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

   

    return render_template('login.html', form=form)

@app.route('/signout', methods=['GET', 'POST'])
def signout():

    logout_user()

    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_login():
    if not admin():
        return "Admin Access Only"
    
    return render_template('admin.html')


#================================================================#

#==========================SIGNUP================================#

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print("Form submitted successfully")  # Print a message when the form is submitted
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
            print("User added to the database")  # Print a message when the user is added to the database
            return redirect(url_for('login'))
        else:
            print("Password confirmation does not match")  # Print a message if password confirmation does not match
    else:
        print("Form validation failed")  # Print a message if form validation fails
        print(form.errors)

    return render_template('signup.html', form=form)


#================================================================#


#==========================Place Order==============================#

@app.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    form = OrderForm()
    if form.validate_on_submit():
        
        #process into DB
        order = Order(
            number = form.number.data,
            creation_date = form.creation_date.data,
            status = form.status.data,
            #select = form.select.data
        )
        
        #store and commit
        db.session.add(orders)
        db.session.commit()

        return redirect(url_for('order_placed'))
    return render_template('place_order.html', form=form)

@app.route('/order_placed') 
def order_placed():
    return "Order Placed Successfully"




#================================================================#

#==========================Products==============================#

products = [
    {
        'code':101,
        'description': '6x8 monocrystalline cell panel, 240W',
        'availability': True,
        'price': 150.00
    },
    {
        'code':202,
        'description': '6x10 monocrystalline cell panel, 310W',
        'availability': True,
        'price': 300.00
    },
    {
        'code':303,
        'description': '6x12 monocrystalline cell panel, 400W',
        'availability': True,
        'price': 450.00
    }
]

# Insert products into the database within the application context
'''
with app.app_context():
    for product_data in products:
        product = Product(
            code=product_data['code'],
            description=product_data['description'],
            availability=product_data['availability'],
            price=product_data['price']
        )
        db.session.add(product)
'''

with app.app_context(): 
    def insert_or_update_product(product):
        stmt = insert(Product).values(
            code=product['code'],
            description=product['description'],
            availability=product['availability'],
            price=product['price']
        )
        on_conflict_stmt = stmt.on_conflict_do_update(
            index_elements=['code'],
            set_={
                'description': stmt.excluded.description,
                'availability': stmt.excluded.availability,
                'price': stmt.excluded.price
            }
        )
        db.session.execute(on_conflict_stmt)

    for product_data in products:
        insert_or_update_product(product_data)

    db.session.commit()

@app.route('/products', methods=['GET'])
@login_required
def products():
    products = Product.query.all() 
    return render_template('products.html', products=products)



#================================================================#