from app import db, app, login
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@login.user_loader
def load_user(id):
    """function has a decorator that provides user authentication 
       and session management. it loads a user based on their id in database

    Args:
        id (int): user id from database

    Returns:
        _type_: model query result
    """
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    """class that creates instance of users table in database 

    Args:
        UserMixin (_type_): Default class that provides implementations
                            for methods expected by Flask-Login
        db (_type_): This class provides database functionality

    Returns:
        _type_: functions to crosscheck specific inputs and 
                string representation
    """
    
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    contact = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    contact_address = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method="pbkdf2:sha1", salt_length=8)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<User {self.username}>"

class Messages(db.Model):
    """class that creates instance of messages table in database 

    Args:
        db (_type_): This class provides database functionality

    """
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(60))
    message = db.Column(db.Text)    
    
class Products(db.Model):
    """class that creates instance of products table in database and
        defines relationship with User class or table

    Args:
        db (_type_): This class provides database functionality

    Returns:
        _type_: string representation
    """
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    creator = db.relationship('User', )
    
    def __repr__(self):
        return f"<Products {self.product_name}-{self.description}"

class Orders(db.Model):
    """class that creates instance of orders table in database 

    Args:
        db (_type_): This class provides database functionality

    """
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    product_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    contact = db.Column(db.String, nullable=False)
    customer_name = db.Column(db.String, nullable=False)
    transaction_id = db.Column(db.String, nullable=False)