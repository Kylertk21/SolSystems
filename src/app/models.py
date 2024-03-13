from app import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    creation_date = db.Column(db.DateTime)
    passwd = db.Column(db.LargeBinary)

class Admin(User): 
    __tablename__ = 'admin_users'
    id = db.Column(db.String, db.ForeignKey("users.id"), primary_key=True)
    name = db.Column(db.String)
    title = db.Column(db.String)
    user = db.relationship("User")

class Customer(User): 
    __tablename__ = 'customer_users'
    id = db.Column(db.String, db.ForeignKey("users.id"), primary_key=True)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    credit_card_info = db.Column(db.Integer)
    user = db.relationship("User")
    orders = db.relationship("Order")

class Order(db.Model): 
    __tablename__ = 'orders'
    number = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime)
    status = db.Column(db.String)
    items_ = db.relationship("Item")
    customer_id = db.Column(db.String, db.ForeignKey("customer_users.id"))

class Item(db.Model): 
    __tablename__ = 'items'
    order = db.Column(db.Integer, db.ForeignKey("orders.number"), primary_key=True)
    seq = db.Column(db.Integer, primary_key=True)
    qtt = db.Column(db.Integer)
    product_code = db.Column(db.String, db.ForeignKey("products.code"))
    product = db.relationship("Product")

class Product(db.Model):
    __tablename__ = 'products'
    code = db.Column(db.String, primary_key=True)
    description = db.Column(db.String)
    type = db.Column(db.String)
    available = db.Column(db.Boolean)
    price = db.Column(db.Float)