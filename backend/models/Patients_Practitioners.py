# models/patient_practitioner.py
from . import db

class PatientPractitioner(db.Model):
    __tablename__ = 'patient_practitioner'
    patient_id = db.Column('Patient_ID', db.Integer, db.ForeignKey('ASD_Patients.Patient_ID', ondelete="CASCADE"), primary_key=True)
    practitioner_id = db.Column('Practitioner_ID', db.Integer, db.ForeignKey('ASD_Practitioners.Practitioner_ID', ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f'<PatientPractitioner Patient {self.patient_id} - Practitioner {self.practitioner_id}>'
