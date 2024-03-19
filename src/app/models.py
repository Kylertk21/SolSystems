from app import db

class User(db.model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.int, primary_key=True)
    name = db.Column(db.String)
    creation_date = db.Column(db.String) #do we need this one ?
    passwd = db.Column(db.LargeBinary)
    # customer and admin can just be objects of this class we just need to figure a way how to difrental betwwen the two

class Admin(User):
    status = db.Column(db.choices)
    submit = db.Column(db.String)
    
class Order():
    __tablename__ = 'orders'
    number = db.Column(db.int, primary_key=True)
    creation_date = db.Column(db.String)
    item = db.Column(db.String) #do we need this one ?
    status = db.Column(db.String)

class Product():
    __tablename__ = 'products'
    code = db.Column(db.int, primary_key=True)
    description = db.Column(db.String)
    availability = db.Colum(db.models.BinaryField(_("False")))
    price = db.Column(db.int, primary_key=True)

    
class Item():
    __tablename__ = 'items'
    sequential_number = db.Column(db.int, primary_key=True)
    quantity = db.Column(db.int, primary_key=True)
    paid_price = db.Column(db.LargeBinary)
