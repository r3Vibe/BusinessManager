from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash

# login form


class Login(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={
                           "placeholder": "Enter Your Username"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={
                             "placeholder": "Enter Your Password"})
    submit = SubmitField("Login")


class productImage(FlaskForm):
    image = FileField("+", validators=[DataRequired()])
    name = StringField("Product Name", validators=[DataRequired()], render_kw={
                       "placeholder": "Enter Product Name"})
    productid = StringField("Product ID", validators=[DataRequired()], render_kw={
                            "placeholder": "Enter Product ID"})
    barcode = StringField("Barcode", render_kw={
                          "placeholder": "Barcode If Any"})
    variations = SelectField("Variations", validators=[
                             DataRequired()], choices=["Select Variation"])
    category = SelectField("Category", validators=[
        DataRequired()], choices=["Select Category"])
    vendor = SelectField("Vendor", validators=[
        DataRequired()], choices=["Select Vendor"])
    quantity = StringField("Quantity", validators=[DataRequired()], render_kw={
                           'placeholder': "Enter Quantity"})
    cost = StringField("Cost", validators=[DataRequired()], render_kw={
                       'placeholder': "Enter Product Cost"})
    sellprice = StringField("Sell Price", validators=[DataRequired()], render_kw={
                            'placeholder': "Enter Selling Price"})
    tax = StringField("Tax", validators=[DataRequired()], render_kw={
                      'placeholder': "Enter Tax %"})
    length = StringField("Length", validators=[DataRequired()], render_kw={
                         'placeholder': "Enter Product Length"})
    bredth = StringField("Breadth", validators=[DataRequired()], render_kw={
                         'placeholder': "Enter Product Breadth"})
    height = StringField("Height", validators=[DataRequired()], render_kw={
                         'placeholder': "Enter Product Height"})
    weight = StringField("Weight", validators=[DataRequired()], render_kw={
                         'placeholder': "Enter Product Weight"})
    submit = SubmitField("Add")
