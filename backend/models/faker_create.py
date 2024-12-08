import os
import random
from faker import Faker
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize dependencies
bcrypt = Bcrypt()
faker = Faker("en_US")  # Restrict data generation to the US locale

# Database connection settings from environment variables
DB_CONFIG = {
    "drivername": "mysql+pymysql",
    "username": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "host": os.getenv("MYSQL_HOST"),
    "port": os.getenv("MYSQL_PORT"),
    "database": os.getenv("MYSQL_DATABASE_NAME"),
}

# Define SSL options
CONNECT_ARGS = {"ssl": {"ssl_mode": os.getenv("MYSQL_SSL_MODE")}}

# Create the SQLAlchemy engine
engine = create_engine(URL.create(**DB_CONFIG), connect_args=CONNECT_ARGS)

# Number of records to generate
num_users = 40
num_patients = 30
num_practitioners = 10
num_sessions = 100
num_relationships = 20

# Define email domains
email_domains = ["gmail.com", "yahoo.com", "sbcglobal.net", "sjsu.edu"]

def reset_and_populate_db():
    # Connect to the database
    with engine.connect() as conn:
        # Start transaction
        with conn.begin():
            # Clear tables
            print("Clearing all tables...")
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            conn.execute(text("TRUNCATE TABLE Sessions;"))
            conn.execute(text("TRUNCATE TABLE patient_practitioner;"))
            conn.execute(text("TRUNCATE TABLE ASD_Practitioners;"))
            conn.execute(text("TRUNCATE TABLE ASD_Patients;"))
            conn.execute(text("TRUNCATE TABLE Users;"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

            print("Inserting new data...")

            # Insert Users
            for user_id in range(1, num_users + 1):
                first_name = faker.first_name().replace("'", "''").lower()
                middle_name = faker.first_name().replace("'", "''")
                last_name = faker.last_name().replace("'", "''").lower()

                # Construct email using first and last names
                domain = random.choice(email_domains)
                email = f"{first_name}.{last_name}@{domain}".replace("'", "''")

                dob = faker.date_of_birth()
                sex = faker.random_element(['Male', 'Female', 'Other'])
                country = "United States"
                street_address = faker.street_address().replace("'", "''")
                city = faker.city().replace("'", "''")
                state = faker.state().replace("'", "''")
                zip_code = faker.zipcode()
                password = "password123"
                # Hash the password
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                conn.execute(text(f"""
                INSERT INTO Users (User_ID, First_Name, Middle_Name, Last_Name, Email_Address, Dob, Sex, Country, Street_Address, City, State, Zip_Code, Password)
                VALUES ({user_id}, '{first_name}', '{middle_name}', '{last_name}', '{email}', '{dob}', '{sex}', '{country}', '{street_address}', '{city}', '{state}', '{zip_code}', '{hashed_password}');
                """))

            # Insert ASD_Patients
            for patient_id in range(1, num_patients + 1):
                user_id = random.randint(1, num_users)
                enrollment_date = faker.date_between(start_date="-1y", end_date="today")
                conn.execute(text(f"""
                INSERT INTO ASD_Patients (Patient_ID, User_ID, Enrollment_Date)
                VALUES ({patient_id}, {user_id}, '{enrollment_date}');
                """))

            # Insert ASD_Practitioners
            for practitioner_id in range(1, num_practitioners + 1):
                user_id = random.randint(1, num_users)
                conn.execute(text(f"""
                INSERT INTO ASD_Practitioners (Practitioner_ID, User_ID)
                VALUES ({practitioner_id}, {user_id});
                """))

            # Insert patient_practitioner relationships
            existing_pairs = set()
            for _ in range(num_relationships):
                while True:
                    patient_id = random.randint(1, num_patients)
                    practitioner_id = random.randint(1, num_practitioners)
                    pair = (patient_id, practitioner_id)
                    if pair not in existing_pairs:  # Ensure unique pairs
                        existing_pairs.add(pair)
                        conn.execute(text(f"""
                        INSERT INTO patient_practitioner (Patient_ID, Practitioner_ID)
                        VALUES ({patient_id}, {practitioner_id});
                        """))
                        break

            # Insert Sessions
            for session_id in range(1, num_sessions + 1):
                patient_id = random.randint(1, num_patients)
                practitioner_id = random.randint(1, num_practitioners)
                session_date = faker.date_time_this_year().strftime('%Y-%m-%d')  # Format to 'YYYY-MM-DD HH:MM:SS'
                session_start_time = faker.time()
                session_end_time = faker.time()
                conn.execute(text(f"""
                INSERT INTO Sessions (Session_ID, Patient_ID, Practitioner_ID, Session_Date, Session_Start_Time, Session_End_Time)
                VALUES ({session_id}, {patient_id}, {practitioner_id}, '{session_date}', '{session_start_time}', '{session_end_time}');
                """))

            print("Data inserted successfully!")

if __name__ == "__main__":
    reset_and_populate_db()
