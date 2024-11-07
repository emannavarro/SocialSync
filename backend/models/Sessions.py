# models/session.py
from . import db

class Session(db.Model):
    __tablename__ = 'Sessions'
    id = db.Column('Session_ID', db.Integer, primary_key=True)
    patient_id = db.Column('Patient_ID', db.Integer, db.ForeignKey('ASD_Patients.Patient_ID', ondelete="CASCADE"), nullable=False)
    practitioner_id = db.Column('Practitioner_ID', db.Integer, db.ForeignKey('ASD_Practitioners.Practitioner_ID', ondelete="CASCADE"), nullable=False)
    session_date = db.Column('Session_Date', db.Date, nullable=False)

    def __repr__(self):
        return f'<Session {self.id} on {self.session_date}>'
