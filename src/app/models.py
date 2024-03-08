class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.int, primary_key=True)
    name = db.Column(db.String)
    creation_date = db.Column(db.String) #do we need this one ?
    passwd = db.Column(db.LargeBinary)
    # customer and admin can just be objects of this class we just need to figure a way how to difrental betwwen the two
    
class Order():
    number = int 
    creation_date = String 
    items = String # should this be a string of products ?
    status = String 

class Product():
    code = int 
    description = String
    availability = False
    price = int
    
class Item():
    sequential_number = int 
    quantity = int 
    paid_price = double 
