from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from .models import Usuario, db

# Criar o blueprint para as rotas
bp = Blueprint('routes', __name__)

@bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo_usuario': usuario.tipo_usuario
    } for usuario in usuarios])

@bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.json
    
    if not dados.get('nome') or not dados.get('email') or not dados.get('senha') or not dados.get('tipo_usuario'):
        return jsonify({'erro': 'Dados inválidos'}), 400
    
    if Usuario.query.filter_by(email=dados.get('email')).first():
        return jsonify({'erro': 'E-mail já cadastrado'}), 400
    
    try:
        senha = generate_password_hash(dados.get('senha'))
        
        novo_usuario = Usuario(
            nome=dados['nome'],
            email=dados['email'],
            senha_hash=senha,
            tipo_usuario=dados['tipo_usuario']
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify({
            "message": "Usuário criado com sucesso",
            "usuario": {
                "id": novo_usuario.id,
                "nome": novo_usuario.nome,
                "email": novo_usuario.email,
                "tipo_usuario": novo_usuario.tipo_usuario
            }
        }), 201
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    
@bp.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo_usuario': usuario.tipo_usuario
    })
