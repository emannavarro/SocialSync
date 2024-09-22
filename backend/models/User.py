# models/user.py
from . import db  # Import the single instance of db from __init__.py

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column('User_ID', db.Integer, primary_key=True)
    first_name = db.Column('First_Name', db.String(255), nullable=False)
    last_name = db.Column('Last_Name', db.String(255), nullable=False)
    email = db.Column('Email_Address', db.String(255), unique=True, nullable=False)
    password = db.Column('Password', db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name} ({self.email})>'
