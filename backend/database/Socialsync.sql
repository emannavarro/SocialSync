-- Select the database for use
USE SocialSyncDB;

-- Drop existing tables to ensure a clean start each time this script is run
DROP TABLE IF EXISTS Sessions;
DROP TABLE IF EXISTS ASD_Practitioners;
DROP TABLE IF EXISTS ASD_Patients;
DROP TABLE IF EXISTS Users;

-- Create Users table
-- Stores user information with a unique Email_Address
CREATE TABLE Users (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(255) NOT NULL,
    Last_Name VARCHAR(255) NOT NULL,
    Email_Address VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Create ASD_Patients table
-- Links to Users via User_ID and cascades on delete
CREATE TABLE ASD_Patients (
    Patient_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT NOT NULL,
    Enrollment_Date DATE NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Create ASD_Practitioners table
-- Each practitioner is linked to a User and assigned Patient; cascades on delete
CREATE TABLE ASD_Practitioners (
    Practitioner_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT NOT NULL,
    Assigned_Patient_ID INT NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Assigned_Patient_ID) REFERENCES ASD_Patients(Patient_ID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Create Sessions table
-- Sessions link to both Practitioners and Patients, cascading on delete
CREATE TABLE Sessions (
    Session_ID INT AUTO_INCREMENT PRIMARY KEY,
    Patient_ID INT NOT NULL,
    Practitioner_ID INT NOT NULL,
    Session_Date DATE NOT NULL,
    Session_Start_Time TIME NOT NULL,
    Session_End_Time TIME NOT NULL,
    FOREIGN KEY (Patient_ID) REFERENCES ASD_Patients(Patient_ID) ON DELETE CASCADE,
    FOREIGN KEY (Practitioner_ID) REFERENCES ASD_Practitioners(Practitioner_ID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Recreate indexes for optimized searching
CREATE INDEX idx_patient ON ASD_Patients(User_ID);
CREATE INDEX idx_practitioner ON ASD_Practitioners(User_ID, Assigned_Patient_ID);
CREATE INDEX idx_sessions ON Sessions(Session_Date, Patient_ID, Practitioner_ID);

-- Insert sample data into the database
INSERT INTO Users (First_Name, Last_Name, Email_Address) VALUES ('John', 'Doe', 'john.doe@example.com');
INSERT INTO Users (First_Name, Last_Name, Email_Address) VALUES ('Jane', 'Smith', 'jane.smith@example.com');
INSERT INTO ASD_Patients (User_ID, Enrollment_Date) VALUES (1, '2023-01-01');
INSERT INTO ASD_Practitioners (User_ID, Assigned_Patient_ID) VALUES (2, 1);
INSERT INTO Sessions (Patient_ID, Practitioner_ID, Session_Date, Session_Start_Time, Session_End_Time) VALUES (1, 1, '2023-01-02', '09:00:00', '10:00:00');

-- Commented test cases below have been tested and verified as of [2023-09-28]
-- Test cases for unique constraints and foreign key relationships
-- INSERT INTO Users (First_Name, Last_Name, Email_Address) VALUES ('Jim', 'Beam', 'john.doe@example.com');
-- INSERT INTO Sessions (Patient_ID, Practitioner_ID, Session_Date, Session_Start_Time, Session_End_Time) VALUES (1, 999, '2023-01-03', '11:00:00', '12:00:00');

-- Functional tests
-- Update a user's email
UPDATE Users SET Email_Address = 'new.john.doe@example.com' WHERE User_ID = 1;
SELECT * FROM Users WHERE User_ID = 1;

-- Cascade delete tests
DELETE FROM Users WHERE User_ID = 2;
