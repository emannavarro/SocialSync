import string
from random import sample

from flask_bcrypt import Bcrypt
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)  # Initialize bcrypt for hashing passwords


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
    __tablename__ = 'Users'  # Use 'Users' to match the actual table name in the database
    id = db.Column('User_ID', db.Integer, primary_key=True)
    first_name = db.Column('First_Name', db.String(255), nullable=False)
    last_name = db.Column('Last_Name', db.String(255), nullable=False)
    email = db.Column('Email_Address', db.String(255), unique=True, nullable=False)
    password = db.Column('Password', db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name} ({self.email})>'

# Register Route to hash and store password securely
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    if not (first_name, last_name, email, password):
        return jsonify({'error': 'Missing information'}), 400

    # Hash password using bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        # Create a new user instance and save to the database
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Basic Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return jsonify({'error': 'Missing email or password'}), 400

    # Fetch the user by email
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # Return basic success message with user info
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8081)))
