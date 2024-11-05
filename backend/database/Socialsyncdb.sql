-- Use the designated database
USE SocialSyncDB;

-- Drop tables in a specific order to respect foreign key relationships
DROP TABLE IF EXISTS patient_practitioner;
DROP TABLE IF EXISTS Sessions;
DROP TABLE IF EXISTS ASD_Practitioners;
DROP TABLE IF EXISTS ASD_Patients;
DROP TABLE IF EXISTS Users;

-- Create the Users table with additional fields as specified in the EER diagram
CREATE TABLE Users (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(255) NOT NULL,
    Middle_Name VARCHAR(255),
    Last_Name VARCHAR(255) NOT NULL,
    Email_Address VARCHAR(255) NOT NULL UNIQUE,
    Dob DATE NOT NULL,
    Sex ENUM('Male', 'Female', 'Other') NOT NULL,
    Country VARCHAR(255) NOT NULL,
    Street_Address VARCHAR(255) NOT NULL,
    City VARCHAR(255) NOT NULL,
    State VARCHAR(255) NOT NULL,
    Zip_Code VARCHAR(10) NOT NULL,
    Password VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

-- Create the ASD_Patients table
CREATE TABLE ASD_Patients (
    Patient_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT NOT NULL,
    Enrollment_Date DATE NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Create the ASD_Practitioners table
CREATE TABLE ASD_Practitioners (
    Practitioner_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID INT NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Create the patient_practitioner table for many-to-many relationships
CREATE TABLE patient_practitioner (
    Patient_ID INT NOT NULL,
    Practitioner_ID INT NOT NULL,
    PRIMARY KEY (Patient_ID, Practitioner_ID),
    FOREIGN KEY (Patient_ID) REFERENCES ASD_Patients(Patient_ID) ON DELETE CASCADE,
    FOREIGN KEY (Practitioner_ID) REFERENCES ASD_Practitioners(Practitioner_ID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Create the Sessions table
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
CREATE INDEX idx_practitioner ON ASD_Practitioners(User_ID);
CREATE INDEX idx_sessions ON Sessions(Session_Date, Patient_ID, Practitioner_ID);

-- Insert sample data into the database
INSERT INTO Users (First_Name, Middle_Name, Last_Name, Email_Address, Password, Dob, Sex, Country, Street_Address, City, State, Zip_Code)
VALUES ('John', 'Quincy', 'Doe', 'john.doe@example.com', 'securepassword', '1990-05-21', 'Male', 'USA', '123 Elm St', 'Anytown', 'CA', '90210');
INSERT INTO Users (First_Name, Middle_Name, Last_Name, Email_Address, Password, Dob, Sex, Country, Street_Address, City, State, Zip_Code)
VALUES ('Jane', NULL, 'Smith', 'jane.smith@example.com', 'securepassword123', '1985-08-15', 'Female', 'USA', '456 Oak St', 'Othertown', 'NY', '10001');

INSERT INTO ASD_Patients (User_ID, Enrollment_Date) VALUES (1, '2023-01-01');
INSERT INTO ASD_Practitioners (User_ID) VALUES (2);

INSERT INTO patient_practitioner (Patient_ID, Practitioner_ID) VALUES (1, 1);
INSERT INTO Sessions (Patient_ID, Practitioner_ID, Session_Date, Session_Start_Time, Session_End_Time)
VALUES (1, 1, '2023-01-02', '09:00:00', '10:00:00');

/*
-- Test cases for unique constraints and foreign key relationships
INSERT INTO Users (First_Name, Last_Name, Email_Address) VALUES ('Jim', 'Beam', 'john.doe@example.com');
INSERT INTO Sessions (Patient_ID, Practitioner_ID, Session_Date, Session_Start_Time, Session_End_Time)
VALUES (1, 999, '2023-01-03', '11:00:00', '12:00:00');

-- Functional tests
UPDATE Users SET Email_Address = 'new.john.doe@example.com' WHERE User_ID = 1;
SELECT * FROM Users WHERE User_ID = 1;

-- Cascade delete tests
DELETE FROM Users WHERE User_ID = 2;
*/

-- Documentation for test cases and validation
-- Unique Constraints: Attempt to insert a duplicate email ('john.doe@example.com') into the Users table.
-- Expected Result: The query should fail with a Duplicate entry error.
-- Foreign Key Relationships: Try to insert a session with an invalid Practitioner_ID.
-- Expected Result: The query should fail with a Cannot add or update a child row error.
-- Cascade Delete Test: Delete a user and ensure all related records in the ASD_Patients, ASD_Practitioners, and Sessions tables are removed.
-- Expected Result: All dependent records should be deleted automatically.
-- Update Test: Update the email of an existing user and ensure that the change is reflected correctly.
