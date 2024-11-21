import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request,jsonify
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask("Google Login App")
app.secret_key = "CodeSpecialist.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "652150480549-iuoe53vbbkdjcgalg963nt0a1k4nt38e.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper

@app.route("/login")
def login():
    # Utilise "prompt=select_account" pour forcer la sélection d'un compte à chaque connexion
    authorization_url, state = flow.authorization_url(prompt="select_account")
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    try:
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
            abort(500)  # State does not match!

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        # Enregistre les informations d'identité dans la session
        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        session["email"] = id_info.get("email")
        session["picture"] = id_info.get("picture")


        return redirect("/protected_area")

    except google.auth.exceptions.InvalidValue as e:
        if "Token expired" in str(e):
            # Redirige vers la connexion pour regénérer un nouveau token si le token est expiré
            return redirect("/login")
        else:
            abort(500)  # Gère d'autres erreurs possibles

@app.route("/logout")
def logout():
    session.clear()  # Efface toute la session pour forcer la déconnexion complète
    return redirect("/")  # Redirige vers la page d'accueil ou de connexion

@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"

@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Profil connecté {session['name']}! <br/>Email :  {session['email']} <br/> <img src='{session['picture']}' alt='photo'/> <a href='/logout'><button>Logout</button></a>"


if __name__ == "__main__":
    app.run(debug=True)
