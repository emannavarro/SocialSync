from . import db
from datetime import time

class Session(db.Model):
    __tablename__ = 'Sessions'
    id = db.Column('Session_ID', db.Integer, primary_key=True)
    patient_id = db.Column('Patient_ID', db.Integer, db.ForeignKey('ASD_Patients.Patient_ID', ondelete="CASCADE"), nullable=False)
    practitioner_id = db.Column('Practitioner_ID', db.Integer, db.ForeignKey('ASD_Practitioners.Practitioner_ID', ondelete="CASCADE"), nullable=False)
    session_date = db.Column('Session_Date', db.Date, nullable=False)
    session_start_time = db.Column('Session_Start_Time', db.Time, nullable=False, default=time(0, 0))
    session_end_time = db.Column('Session_End_Time', db.Time, nullable=False, default=time(0, 0))

    def __repr__(self):
        return f'<Session {self.id} on {self.session_date} at {self.session_start_time}>'
