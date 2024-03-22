from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    creation_date = db.Column(db.String)
    passwd = db.Column(db.LargeBinary)
    role = db.Column(db.Boolean, default=False)


'''class Admin(User):
    id = db.Column(db.String, db.ForeignKey('users.id'), primary_key=True)
    order = db.Column(db.String(50), nullable=False)

    def get_orders(): #retrieve list of orders
        form = Order()
        return form.order.choices'''

class Customer(User):
    id = db.Column(db.String, db.ForeignKey('users.id'), primary_key=True)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    credit_card_info = db.Column(db.String)
    
class Order(db.Model):
    __tablename__ = 'orders'
    number = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.String)
    item = db.Column(db.String)
    status = db.Column(db.String)

class Product(db.Model):
    __tablename__ = 'products'
    code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    availability = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float)


class Item(db.Model):
    __tablename__ = 'items'
    sequential_number = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, primary_key=True)
    paid_price = db.Column(db.LargeBinary)
