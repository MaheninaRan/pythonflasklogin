from flask import Blueprint, jsonify, request, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from app.models.models import db
from app.models.login import Login

# Création du Blueprint pour le contrôleur login
login_bp = Blueprint('login', __name__)

# Configuration du blueprint Google OAuth
google_bp = make_google_blueprint(
    client_id="1008945689071-7rojkvcm7hnq0n11r2drh2siusnuooj7.apps.googleusercontent.com",
    client_secret="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",
    redirect_to="login.google_authorized"
)

# Assurez-vous d'enregistrer google_bp dans __init__.py également.

# Route pour gérer la connexion Google
@login_bp.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    return redirect(url_for('login.google_authorized'))

# Route pour gérer la redirection après l'authentification Google
@login_bp.route('/google_login/google/authorized')
def google_authorized():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    resp = google.get('/userinfo/v2/me')
    if not resp.ok:
        return "Erreur lors de la récupération des informations", 500
    
    info = resp.json()
    email = info.get("email")
    name = info.get("name")

    # Vérifier si l'utilisateur existe dans la base de données, sinon l'ajouter
    user = Login.query.filter_by(email=email).first()
    if not user:
        new_user = Login(email=email, mdp="GoogleOAuth")
        db.session.add(new_user)
        db.session.commit()

    return jsonify({"message": f"Connecté en tant que: {name} ({email})"})

# Route pour gérer les connexions par formulaire (par exemple, via email et mot de passe)
@login_bp.route('/login/facebook', methods=['POST'])
def create_categorie():
    data = request.get_json()
    email = data.get('email')
    mdp = data.get('mdp')
    new_login = Login(email=email, mdp=mdp)
    db.session.add(new_login)
    db.session.commit()
    return jsonify({"message": "Utilisateur enregistré avec succès"})

