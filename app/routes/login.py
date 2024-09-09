from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from ..models import Usuario, db

login_bp = Blueprint('login',__name__)

@login_bp.route('/login', methods =['POST'])
def login():
    dados = request.json

    if not dados.get('email') or not dados.get('senha'):
        return jsonify({'erro':'Email e senha são obrigatórios'}),400
    
    user = Usuario.query.filter_by(email = dados.get('email')).first();
        
    if user and check_password_hash(user.senha_hash, dados.get('senha')):
        # gerar um token de acesso JWT com o ID do usuario
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    
    else:
        return jsonify({'erro':'Credenciais inválidas'}), 401
    
    

    
    
