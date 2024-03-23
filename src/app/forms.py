from flask_wtf import FlaskForm
from wtforms import FormField, BooleanField, DecimalField, FieldList, IntegerField, StringField, PasswordField, TextAreaField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
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
    products = FieldList(FormField(ProductForm), min_entries=1)
    submit = SubmitField('Place Order')

    '''def copy(self):
        copied_form = OrderForm()
        for field_name, field in self._fields.items():
            if field_name in self.data:
                setattr(copied_form, field_name, self.data[field_name])
        copied_form.errors.update(self.errors)
        return copied_form'''

class OrderStatusForm(FlaskForm):
    order_id = StringField('Order ID', validators=[DataRequired()])
    status = SelectField('Order Status', choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped')], validators=[DataRequired()])
    submit = SubmitField('Change Order Status')

class ProductUpdateForm(FlaskForm):
    code = IntegerField('Code', validators=[DataRequired()])
    description = StringField('Description')
    availability = BooleanField('Availability')
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Update Product')

class AdminForm(FlaskForm):
    update_product_catalog = FormField(ProductUpdateForm)
    change_order_status = FormField(OrderStatusForm)
