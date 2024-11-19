from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patient'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    dtn = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f'<Patient {self.nom}>'

