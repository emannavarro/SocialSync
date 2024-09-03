import string
from random import random

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from sqlalchemy import text

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Construct the SQLAlchemy Database URI using the environment variables
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
database = os.getenv('MYSQL_DATABASE_NAME')
ssl_mode = os.getenv('MYSQL_SSL_MODE')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

# Initialize the database
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'  # Make sure the table name matches your actual table name

    id = db.Column('User_ID', db.Integer, primary_key=True)
    first_name = db.Column('First_Name', db.String(80), nullable=False)
    last_name = db.Column('Last_Name', db.String(80), nullable=False)
    email = db.Column('Email_Address', db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name} ({self.email})>'



# Function to generate a random string
def generate_random_string(length=8):
    return ''.join(random.sample(string.ascii_letters + string.digits, k=length))



# Flask route to create a user with the name "John Doe"
@app.route('/test', methods=['POST', 'GET'])
def create_john_doe():
    first_name = "John"
    last_name = "Doe"
    email = "john.doe@example.com"

    # Construct the SQL INSERT query
    insert_query = text("""
        INSERT INTO Users (First_Name, Last_Name, Email_Address)
        VALUES (:first_name, :last_name, :email)
    """)

    # Execute the query
    db.session.execute(insert_query, {'first_name': first_name, 'last_name': last_name, 'email': email})
    db.session.commit()

    return jsonify({
        'message': 'John Doe created successfully!',
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    })
@app.route('/delete_user/<int:uid>')
def delete_user(uid):
    db.session.execute(text("DELETE FROM users WHERE id = :uid"), {'uid': uid})
    db.session.commit()
    return f"User with id {uid} deleted successfully!"

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8081)))
