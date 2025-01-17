from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField,PasswordField, validators, SubmitField, TextAreaField, FloatField, FileField, SelectField
from wtforms.validators import DataRequired

class Register(FlaskForm):
    """This class defines form variables mapped with specific fieldtypes
       integrating FlaskForm additional features

    Args:
        FlaskForm (object): a class in Flask-WTF which gives additional
                           features like CSRF, validation, error handling etc
    """
    username = StringField("Enter Your name", [validators.DataRequired(message="Please enter a username")])
    contact = TelField("Enter yout phone number", [validators.DataRequired(message="Please enter a contact")])
    email = EmailField('Enter yout email address', [validators.Email(message="Please enter a valid email!!! ")])
    contact_address = StringField("Enter your delivery address", [validators.DataRequired(message="Please enter a contact address!!")])
    password = PasswordField("Enter a password of your choice", [validators.DataRequired(message="Please use a strong combination"), validators.Length(min=7,max=15)])
    confirm_password = PasswordField("Confirm passowrd", [validators.DataRequired(message="Re-enter password"), validators.EqualTo('password', message="Mismatched-password")])
    submit = SubmitField("Sign Up!!")
    
class Login(FlaskForm):
    """This class defines form variables mapped with specific fieldtypes
       integrating FlaskForm additional features

    Args:
        FlaskForm (object): a class in Flask-WTF which gives additional
                           features like CSRF, validation, error handling etc
    """
    email = EmailField("Enter your email address", [validators.DataRequired(message="Please your email address!!!")], render_kw={"error_color": "red"} )
    password = PasswordField("Enter your password", [validators.DataRequired(message="Please enter your password")], render_kw={"error_color": "red"})
    submit = SubmitField('Login!!')

class Contact(FlaskForm):
    """This class defines form variables mapped with specific fieldtypes
       integrating FlaskForm additional features

    Args:
        FlaskForm (object): a class in Flask-WTF which gives additional
                           features like CSRF, validation, error handling etc
    """
    name = StringField("Enter your name", [validators.DataRequired(message="Please enter a name!!!")])
    email = EmailField("Provide your email address", [ validators.DataRequired(message="Please enter an email address!!!")])
    message = TextAreaField("Write your message", [validators.DataRequired("Please enter a message!!!")])
    submit = SubmitField("Send!!")

class Stocks(FlaskForm):
    """This class defines form variables mapped with specific fieldtypes
       integrating FlaskForm additional features

    Args:
        FlaskForm (object): a class in Flask-WTF which gives additional
                           features like CSRF, validation, error handling etc
    """
    name = StringField("Enter product name", [validators.DataRequired(message="Product name is essential!!!")])
    price = FloatField("Enter product price", [validators.DataRequired(message="Product Price is needed!!!")])
    category = SelectField('Category', 
                           choices=[('men', "Men's Shoes"), 
                                    ('women', "Women's Shoes"), 
                                    ('sports', 'Sports Shoes'), 
                                    ('kids', "Kids' Shoes")], 
                           validators=[DataRequired()])
    description = TextAreaField("Give a brief product description", [validators.DataRequired()])
    image = FileField("Picture of product", [validators.DataRequired(message="Please provide product image")])
    submit = SubmitField("Add Product")
    