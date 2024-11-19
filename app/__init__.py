from flask_cors import CORS
from flask import Flask 
from config import config
from app.models.models import db


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)  # Permettre les requêtes cross-origin

    from .routes import main
    
    from .controller.loginController import login_bp
    app.register_blueprint(main)
    app.register_blueprint(login_bp)

    
    CORS(app)
    
    return app
