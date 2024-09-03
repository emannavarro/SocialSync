from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy import text

app = Flask(__name__)

# Configure MySQL Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysecretpassword@localhost:3306/SocialSyncDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Create the tables in the database
with app.app_context():
    db.create_all()



# Example route to create a new user
@app.route('/create_user')
def create_user():
    new_user = User(username="testuser", email="test@example.com")
    db.session.add(new_user)
    db.session.commit()
    return f'User {new_user.username} created!'

@app.route('/delete_user/<int:uid>')
def delete_user():
    new_user = User(username="testuser", email="test@example.com")
    db.session.execute(text("DELETE FROM Users WHERE User_ID = 1"))
    db.session.commit()
    return "Success"

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))

