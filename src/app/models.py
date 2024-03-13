class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.int, primary_key=True)
    name = db.Column(db.String)
    creation_date = db.Column(db.String) #do we need this one ?
    passwd = db.Column(db.LargeBinary)
    # customer and admin can just be objects of this class we just need to figure a way how to difrental betwwen the two
    
class Order():
    number = db.Column(db.int, primary_key=True)
    creation_date = db.Column(db.String)
    item = db.Column(db.String) #do we need this one ?
    satus = db.Column(db.String)

class Product():
    code = db.Column(db.int, primary_key=True)
    description = db.Column(db.String)
    availability = db.Colum(db.models.BinaryField(_("False")))
    price = db.Column(db.int, primary_key=True)

    
class Item():
    sequential_number = db.Column(db.int, primary_key=True)
    quantity = db.Column(db.int, primary_key=True)
    paid_price = db.Column(db.LargeBinary)
