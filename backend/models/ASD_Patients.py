# models/asd_patient.py
from . import db

class ASDPatient(db.Model):
    __tablename__ = 'ASD_Patients'
    id = db.Column('Patient_ID', db.Integer, primary_key=True)
    user_id = db.Column('User_ID', db.Integer, db.ForeignKey('Users.User_ID', ondelete="CASCADE"), nullable=False)
    enrollment_date = db.Column('Enrollment_Date', db.Date, nullable=False)

    def __repr__(self):
        return f'<ASDPatient {self.id} (User ID: {self.user_id})>'
