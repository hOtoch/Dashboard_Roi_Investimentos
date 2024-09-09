from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Usuario, db

# Definir o blueprint para rotas de usuários
usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    
    if usuario.tipo_usuario != 'admin':
        return jsonify({'erro': 'Você não tem permissão para acessar esta rota'}),403
    
    
    usuarios = Usuario.query.all()
    return jsonify([{
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo_usuario': usuario.tipo_usuario
    } for usuario in usuarios])
    

@usuarios_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.json
    if not dados.get('nome') or not dados.get('email') or not dados.get('senha') or not dados.get('tipo_usuario'):
        return jsonify({'erro': 'Dados inválidos'}), 400
    
    if Usuario.query.filter_by(email=dados.get('email')).first():
        return jsonify({'erro': 'E-mail já cadastrado'}), 400
    
    try:
        senha = generate_password_hash(str(dados.get('senha')))
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


@usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
@jwt_required()
def buscar_usuario(id):
    usuario_logado_id = get_jwt_identity()
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    if usuario_logado_id != usuario.id and Usuario.query.get(usuario_logado_id).tipo_usuario != 'admin':
        return jsonify({'erro': 'Você não tem permissão para acessar este recurso'}), 403
    
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo_usuario': usuario.tipo_usuario
    })
    
    
@usuarios_bp.route('/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(id):
    usuario_logado_id = get_jwt_identity()
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

    # Verificar se o usuário tem permissão para atualizar (admin pode editar qualquer um, usuário comum só pode editar seu próprio perfil)
    if usuario.id != usuario_logado_id and Usuario.query.get(usuario_logado_id).tipo_usuario != 'admin':
        return jsonify({'erro': 'Você não tem permissão para atualizar este recurso'}), 403

    dados = request.json
    if dados.get('nome'):
        usuario.nome = dados['nome']
    
    if dados.get('email'):
        usuario.email = dados['email']
    
    if dados.get('senha'):
        usuario.senha_hash = generate_password_hash(str(dados['senha']))

    db.session.commit()

    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'tipo_usuario': usuario.tipo_usuario
    })

    
@usuarios_bp.route('/usuarios/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_usuario(id):
    usuario_logado_id = get_jwt_identity()
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    if Usuario.query.get(usuario_logado_id).tipo_usuario != 'admin':
        return jsonify({'erro': 'Você não tem permissão para deletar este usuário'}), 403
    
    db.session.delete(usuario)
    db.session.commit()
    
    return jsonify({'message': 'Usuário deletado com sucesso'})
    
    