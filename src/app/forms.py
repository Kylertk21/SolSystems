from flask_wtf import FlaskForm, Form
from wtforms import StringField, IntegerField, FieldList, FormField, SelectField, PasswordField, TextAreaField, DateField, SubmitField, validators
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class SignInForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class OrderForm(FlaskForm):
    product = StringField('Product', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Place Order')
    
class OrderStatus(FlaskForm):
    status = SelectField('Order Status', choices=[('pending', 'processing', 'shipped')])
    submit = SubmitField('Change Order Status')
    
class ProductForm(FlaskForm):
    code = StringField('Product Code', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Add Product')
