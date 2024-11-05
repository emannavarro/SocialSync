# app.py
import os
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from models import db  # Import the single db instance
from models.User import User  # Import the User model

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Construct the SQLAlchemy Database URI using the environment variables
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
database = os.getenv('MYSQL_DATABASE_NAME')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

# Initialize the db with the app
db.init_app(app)

# Ensure tables are created within the app context
with app.app_context():
    db.create_all()

# Register Route to hash and store password securely
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    first_name = data.get('first_name')
    middle_name = data.get('middle_name')
    last_name = data.get('last_name')
    email = data.get('email')
    dob = data.get('dob')
    sex = data.get('sex')
    country = data.get('country')
    street_address = data.get('street_address')
    city = data.get('city')
    state = data.get('state')
    zip_code = data.get('zip_code')
    password = data.get('password')

    # Check for required fields
    required_fields = [first_name, last_name, email, dob, sex, country, street_address, city, state, zip_code, password]
    if not all(required_fields):
        return jsonify({'error': 'Missing information'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create new User instance
    try:
        new_user = User(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            dob=dob,
            sex=sex,
            country=country,
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            password=hashed_password
        )
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

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/getusers', methods=['GET'])
def Getuser():
    try:
        users = User.query.all()  # Get all user records
        # Prepare a list of dictionaries for each user
        user_list = [
            {
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            } for user in users
        ]
        return jsonify({
            'message': 'Users retrieved successfully',
            'users': user_list
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8081)))
