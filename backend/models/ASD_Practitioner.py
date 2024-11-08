# models/asd_practitioner.py
from . import db

class ASDPractitioner(db.Model):
    __tablename__ = 'ASD_Practitioners'
    id = db.Column('Practitioner_ID', db.Integer, primary_key=True)
    user_id = db.Column('User_ID', db.Integer, db.ForeignKey('Users.User_ID', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'<ASDPractitioner {self.id} (User ID: {self.user_id})>'
