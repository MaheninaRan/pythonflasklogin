# models/login.py
from flask_sqlalchemy import SQLAlchemy
from .models import db
from flask import jsonify


class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    mdp = db.Column(db.String(255), nullable=False)

    def __init__(self, email, mdp):
        self.email = email
        self.mdp = mdp

    def __repr__(self):
        return f'<Login {self.email}, {self.mdp}>'
