'''
CS3250 - Software Development Methods and Tools - Spring 2024
Instructor: Thyago Mota
Team: 2
Description: Project 1 - Sol Systems Web App
'''

from flask import Flask
import os, bcrypt
from datetime import datetime

app = Flask("Sol Systems")
app.secret_key = os.environ['SECRET_KEY']

# db initialization
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

from app import models
with app.app_context(): 
    db.create_all()

# login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

# user_loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None

from app import routes