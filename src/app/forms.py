from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    creation_date = StringField('Creation Date', 
                                validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class LoginForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')
    
class OrderForm(FlaskForm):
    order = SelectField('Order', choices=[('order1', 'Order 1'), ('order2', 'Order 2'), ('order3', 'Order 3'), ('order4', 'Order 4')], validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Place Order')
    
class OrderStatus(FlaskForm):
    status = SelectField('Order Status', choices=[('pending', 'processing', 'shipped')])
    submit = SubmitField('Change Order Status')
    
class ProductForm(FlaskForm):
    item = StringField('Item', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

