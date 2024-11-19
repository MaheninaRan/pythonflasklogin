import os

class Config:
    """Configuration de base."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une_clé_secrète_très_difficile_à_deviner'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'postgresql://postgres.teqhfbulenvestvxiehf:1766Mahenina@aws-0-us-east-1.pooler.supabase.com:6543/postgres'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Ajoute d'autres configurations ici selon tes besoins
    
    # Configuration des sessions
    SESSION_TYPE = 'filesystem'  # Utilise le système de fichiers pour stocker les sessions
    SESSION_PERMANENT = False    # Les sessions ne sont pas permanentes par défaut
    SESSION_USE_SIGNER = True    # Utilise un signataire pour les cookies de session pour plus de sécurité
    SESSION_FILE_DIR = os.path.join(os.getcwd(), 'flask_session')  # Dossier pour stocker les sessions si `SESSION_TYPE` est 'filesystem'
    SESSION_FILE_THRESHOLD = 500  # Limite le nombre de fichiers de session sur le disque

class DevelopmentConfig(Config):
    """Configuration pour le développement."""
    DEBUG = True

class TestingConfig(Config):
    """Configuration pour les tests."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class ProductionConfig(Config):
    """Configuration pour la production."""
    DEBUG = False
    # Autres configurations spécifiques à la production

# Un dictionnaire pour facilement accéder aux configurations
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
