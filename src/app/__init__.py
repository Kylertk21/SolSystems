'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Team:
Description: Project 1 - Sol Systems Web App
'''

from flask import Flask
import os

app = Flask("Sol Systems Web App")
app.secret_key = 'secret'
app.config['USER SIGN UP']= 'User Sign UP"'
app.config['USER SIGNIN']= 'User Sign IN"'

#db init
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://app.db'
db.init(app)

from app import models
with app.app.context():
    db.create_all()

#login
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

#callback
@login_manager.user_loader
def load_user(id):
    try:
        return db.session.query(User).filter(User.id==id).one()
    except:
        return None
    
from app import routes












# hard code 
user1 = User(id=1, name='John ', passwd=b'my_secure_password')
order1 = Order(number=21, creation_date='2024-03-09', items='ProductA, ProductB', status='Pending')
product1 = Product(code=1, description='ProductA', availability=True, price=10)
item1 = Item(sequential_number=1, quantity=2, paid_price=20.0)
pass