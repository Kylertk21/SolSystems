'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Team: 2
Description: Project 1 - Sol Systems Web App
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask("Sol Systems Web App")
csrf = CSRFProtect(app)
app.secret_key = 'secret'
app.config['USER_SIGN_UP'] = 'User Sign Up'
app.config['USER_SIGN_IN'] = 'User Sign In'

# Initialize Flask-SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)


# Initialize Flask-Login
login_manager = LoginManager(app)

# Import routes
from . import routes

# Import models
from .models import User, Order, Product, Item

# Create database tables
with app.app_context():
    db.create_all()

# callback
@login_manager.user_loader
def load_user(id):
    try:
        return db.session.query(User).filter(User.id == id).one()
    except:
        return None

# hard code 
    '''
user1 = User(id=1, name='John ', passwd=b'my_secure_password')
order1 = Order(number=21, creation_date='2024-03-09', item='ProductA, ProductB', status='Pending')
product1 = Product(code=1, description='ProductA', availability=True, price=10)
item1 = Item(sequential_number=1, quantity=2, paid_price=20.0)'''
