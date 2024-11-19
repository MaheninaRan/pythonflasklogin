from flask import Blueprint, jsonify,request
from app.models.categorie import Categorie,allCategorie,categerie_byId
from app.models.commande import Commande
from app.models.commande_description import Commande_description
from app.models.produit import Produit,get_date_dernier_entrer,allproduit,produit_by_id
from app.models.models import db
from sqlalchemy import text
from app.models.mouvement_stock_produit import Mouvement_stock_produit
from app.models.users_client import Users_Client
from sqlalchemy import func


produit_bp = Blueprint('produit', __name__)

@produit_bp.route('/produit/insert', methods=['POST'])
def create_categorie():
    data = request.get_json()
    nom = data.get('nom')
    prix = data.get('prix')
    idcategorie = data.get('id_categorie')
    image=data.get('image')
    caracteristique = data.get('caracteristique')
    new_produit = Produit(nom=nom,prix=prix,categorie_id=idcategorie,caracteristique=caracteristique,image=image)
    db.session.add(new_produit)
    db.session.commit()
    return jsonify({
        'id': new_produit.id,
        'nom': new_produit.nom,
        'prix': new_produit.prix,
        'idcategorie':new_produit.categorie.id,
        'categorie': new_produit.categorie.nom,  
        'caracteristique': new_produit.caracteristique
    }), 200
    