from faker import Faker
import random

faker = Faker()

# Number of records to generate
num_users = 10
num_patients = 5
num_practitioners = 3
num_sessions = 8
num_relationships = 5

# Initialize the SQL script
sql_script = []

# Generate Users
sql_script.append("-- Insert Users")
for user_id in range(1, num_users + 1):
    first_name = faker.first_name().replace("'", "''")
    middle_name = faker.first_name().replace("'", "''")
    last_name = faker.last_name().replace("'", "''")
    email = faker.unique.email().replace("'", "''")
    dob = faker.date_of_birth()
    sex = faker.random_element(['Male', 'Female', 'Other'])
    country = faker.country().replace("'", "''")
    street_address = faker.street_address().replace("'", "''")
    city = faker.city().replace("'", "''")
    state = faker.state().replace("'", "''")
    zip_code = faker.zipcode()
    password = "password123"

    sql_script.append(f"""
    INSERT INTO Users (User_ID, First_Name, Middle_Name, Last_Name, Email_Address, Dob, Sex, Country, Street_Address, City, State, Zip_Code, Password)
    VALUES ({user_id}, '{first_name}', '{middle_name}', '{last_name}', '{email}', '{dob}', '{sex}', '{country}', '{street_address}', '{city}', '{state}', '{zip_code}', '{password}');
    """)

# Generate ASD_Patients
sql_script.append("-- Insert ASD_Patients")
for patient_id in range(1, num_patients + 1):
    user_id = random.randint(1, num_users)
    enrollment_date = faker.date_between(start_date="-1y", end_date="today")
    sql_script.append(f"""
    INSERT INTO ASD_Patients (Patient_ID, User_ID, Enrollment_Date)
    VALUES ({patient_id}, {user_id}, '{enrollment_date}');
    """)

# Generate ASD_Practitioners
sql_script.append("-- Insert ASD_Practitioners")
for practitioner_id in range(1, num_practitioners + 1):
    user_id = random.randint(1, num_users)
    sql_script.append(f"""
    INSERT INTO ASD_Practitioners (Practitioner_ID, User_ID)
    VALUES ({practitioner_id}, {user_id});
    """)

# Generate patient_practitioner relationships
sql_script.append("-- Insert patient_practitioner Relationships")
for _ in range(num_relationships):
    patient_id = random.randint(1, num_patients)
    practitioner_id = random.randint(1, num_practitioners)
    sql_script.append(f"""
    INSERT INTO patient_practitioner (Patient_ID, Practitioner_ID)
    VALUES ({patient_id}, {practitioner_id});
    """)

# Generate Sessions
sql_script.append("-- Insert Sessions")
for session_id in range(1, num_sessions + 1):
    patient_id = random.randint(1, num_patients)
    practitioner_id = random.randint(1, num_practitioners)
    session_date = faker.date_time_this_year()
    session_start_time = faker.time()
    session_end_time = faker.time()
    sql_script.append(f"""
    INSERT INTO Sessions (Session_ID, Patient_ID, Practitioner_ID, Session_Date, Session_Start_Time, Session_End_Time)
    VALUES ({session_id}, {patient_id}, {practitioner_id}, '{session_date}', '{session_start_time}', '{session_end_time}');
    """)

# Save to SQL file
with open("faker_generated_data.sql", "w") as f:
    f.write("\n".join(sql_script))

print("SQL script generated: faker_generated_data.sql")
