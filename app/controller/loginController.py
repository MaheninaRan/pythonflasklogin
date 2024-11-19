from flask import Blueprint, jsonify,request
from app.models.models import db
from app.models.login import Login
from sqlalchemy import text
from sqlalchemy import func


login_bp = Blueprint('login', __name__)

@login_bp.route('/login/facebook', methods=['POST'])
def create_categorie():
    data = request.get_json()
    email = data.get('email')
    mdp = data.get('mdp')
    new_login = Login(email,mdp)
    db.session.add(new_login)
    db.session.commit()
    return jsonify({"Mety":"MEty"})
    