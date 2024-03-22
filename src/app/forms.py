from flask_wtf import FlaskForm
from wtforms import FormField, BooleanField, DecimalField, FieldList, IntegerField, StringField, PasswordField, TextAreaField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    creation_date = StringField('Creation Date', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class LoginForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')


class ProductForm(FlaskForm):
    code = IntegerField('Code', validators=[DataRequired()])
    description = StringField('Description')
    availability = BooleanField('Availability')
    price = StringField('Price', validators=[DataRequired()])
    
class Item(FlaskForm):
    sequential_number = IntegerField('Sequential Number', validators=[DataRequired()]) 
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price_paid = DecimalField('Price Paid', validators=[DataRequired()])
    product = FormField(ProductForm)
    
class OrderForm(FlaskForm):
    number = IntegerField('Number', validators=[DataRequired()])
    creation_date = StringField('Creation Date', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    #items = FieldList(FormField(Item))
    #select = SelectField('Order', choices=[('order1', 'Order 1'), ('order2', 'Order 2'), ('order3', 'Order 3'), ('order4', 'Order 4')], validators=[DataRequired()])
    #quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Place Order')

class OrderStatus(FlaskForm):
    order_id = StringField('Order ID')
    status = SelectField('Order Status', choices=[('pending', 'processing', 'shipped')])
    submit = SubmitField('Change Order Status')

class AdminForm(FlaskForm):
    update_product_catalog = FormField(OrderStatus)
    change_order_status = FormField(OrderStatus) 




