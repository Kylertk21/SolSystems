from flask import render_template, redirect, url_for, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Product, Order 

app = Flask(__name__)
app.secret_key = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


users = {
    1: {'id': 'tmota', 'username': 'tmota', 'password': '1', 'is_admin': True}
}

products = {
    1: {'code': 101, 'description': '6x8 monocrystalline cell panel, 240W', 'availability': True, 'price': 150.00},
    2: {'code': 202, 'description': '6x10 monocrystalline cell panel, 310W', 'availability': True, 'price': 300.00},
    3: {'code': 303, 'description': '6x12 monocrystalline cell panel, 400W', 'availability': True, 'price': 450.00}
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            next_page = request.args.get('next') 
            return redirect(next_page or url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    else:
        products = Product.query.all()
        return render_template('place_order.html', products=products)
    
@app.route('/track_order/<order_number>')
@login_required
def track_order(order_number):
    order = next((o for o in orders.values() if o['number'] == order_number), None)
    if order and (current_user.is_admin or order['customer_id'] == current_user.id):
        return render_template('track_order.html', order=order)
    else:
        return redirect(url_for('dashboard'))
    
@app.route('/update_catalog', methods=['GET', 'POST'])
@login_required
def update_catalog():
    if current_user.is_admin:
        if request.method == 'POST':
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('update_catalog.html', products=products.values())
    else:
        return redirect(url_for('dashboard'))    

@app.route('/change_order_status/<order_number>', methods=['POST'])
@login_required
def change_order_status(order_number):
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('dashboard'))

    if __name__ == '__main__':
        app.run(debug=True)