from flask import Blueprint, jsonify, request
from ..models import CicloMes,Usuario,Dia, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..routes.contas import atualizar_todas_contas
from sqlalchemy import func

ciclomes_bp = Blueprint('ciclomes', __name__)

def soma_alcancado_dias(ciclomes):
  soma = db.session.query(func.sum(Dia.alcancado_dia)).filter(Dia.mes_id == ciclomes.id).scalar()
  return soma

def soma_juros_dias(ciclomes):
  soma = db.session.query(func.sum(Dia.juros)).filter(Dia.mes_id == ciclomes.id).scalar()
  return soma


def aplicar_regras_negocio(ciclomes):
    ciclomes.alcancado = soma_alcancado_dias(ciclomes)
    ciclomes.projecao = soma_juros_dias(ciclomes)
    
    if ciclomes.projecao and ciclomes.projecao != 0:
        ciclomes.porcentagem_alcancado = ciclomes.alcancado / ciclomes.projecao
    else:
        ciclomes.porcentagem_alcancado = 0 
    

def atualizar_ciclomes(ciclomes_id):
    ciclomes = CicloMes.query.get(ciclomes_id)
    aplicar_regras_negocio(ciclomes=ciclomes)
    
def criar_dias(ciclomes):
    qtd_dias = ciclomes.dias
    saldo_atual = ciclomes.investimento
    
    for i in range(1,qtd_dias+1):
        
        try:
            juros_atual = saldo_atual * ciclomes.shark
            dia = Dia(
                mes_id = ciclomes.id,
                saldo_inicial = saldo_atual,
                juros = juros_atual,
                alcancado_dia = 0.0
            )

            db.session.add(dia)
            db.session.commit()
            
            saldo_atual += juros_atual
         
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 500
        
    return "Dias criados"


@ciclomes_bp.route('/api/ciclomes', methods=['POST'])
@jwt_required()
def criar_ciclomes():
    dados = request.json
    
    usuario_id_logado = get_jwt_identity()
    
    usuario = Usuario.query.get(usuario_id_logado)
    
    if not usuario.tipo_usuario == 'admin':
        return jsonify({'erro': 'Você não tem permissão para criar o ciclo de um mês'})

    # Verificar se todos os dados necessários foram enviados
    if not dados.get('nome') or not dados.get('dias') or not dados.get('ano') or not dados.get('investimento'):
        return jsonify({'erro': 'Dados inválidos ou incompletos'}), 400

    try:
        # Criar novo CicloMes
        novo_ciclomes = CicloMes(
            nome=dados['nome'],
            ano=dados['ano'],
            investimento=dados['investimento'],
            dias=dados['dias'],
            shark=dados['shark'],
            valor_liquido=dados['valor_liquido']
        )
        
        db.session.add(novo_ciclomes)
        db.session.commit()
        
        criar_dias(novo_ciclomes)
        
        aplicar_regras_negocio(novo_ciclomes)
        
        db.session.commit()
        
        return jsonify({
            "message": "CicloMes criado com sucesso",
            "ciclomes": {
                "id": novo_ciclomes.id,
                "nome": novo_ciclomes.nome,
                "ano": novo_ciclomes.ano,
                "investimento": novo_ciclomes.investimento,
                "dias": novo_ciclomes.dias,
                "shark": novo_ciclomes.shark,
                "alcancado": novo_ciclomes.alcancado,
                "projecao": novo_ciclomes.projecao,
                "porcentagem_alcancado": novo_ciclomes.porcentagem_alcancado,
                "valor_liquido": novo_ciclomes.valor_liquido
            }
        }), 201

    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    
@ciclomes_bp.route('/api/ciclomes/<int:id>', methods=['GET'])
@jwt_required()
def acessar_ciclomes(id):
    # Buscar o CicloMes pelo ID
    ciclomes = CicloMes.query.get(id)

    if not ciclomes:
        return jsonify({'erro': 'CicloMes não encontrado'}), 404

    # Retornar os dados do CicloMes
    return jsonify({
        'id': ciclomes.id,
        'nome': ciclomes.nome,
        'ano': ciclomes.ano,
        'investimento': ciclomes.investimento,
        'dias': ciclomes.dias,
        'shark': ciclomes.shark,
        'alcancado': ciclomes.alcancado,
        'projecao': ciclomes.projecao,
        'porcentagem_alcancado': ciclomes.porcentagem_alcancado,
        'valor_liquido': ciclomes.valor_liquido,
        'atual' : ciclomes.atual
    }), 200


@ciclomes_bp.route('/api/ciclomes/<int:id>', methods=['PUT'])
@jwt_required()
def editar_ciclomes(id):
    
    usuario_id_logado = get_jwt_identity()
    
    usuario = Usuario.query.get(usuario_id_logado)
    
    if not usuario.tipo_usuario == 'admin':
        return jsonify({'erro': 'Você não tem permissão para editar o ciclo de um mês'})
    
    ciclomes = CicloMes.query.get(id)

    if not ciclomes:
        return jsonify({'erro': 'CicloMes não encontrado'}), 404

    dados = request.json

    # Atualizar os dados
    if 'nome' in dados:
        ciclomes.nome = dados['nome']
    if 'ano' in dados:
        ciclomes.ano = dados['ano']    
    if 'investimento' in dados:
        ciclomes.investimento = dados['investimento']
    if 'dias' in dados:
        ciclomes.dias = dados['dias']
    if 'shark' in dados:
        ciclomes.shark = dados['shark']
    if 'alcancado' in dados:
        ciclomes.alcancado = dados['alcancado']
    if 'valor_liquido' in dados:
        ciclomes.valor_liquido = dados['valor_liquido']
        
    aplicar_regras_negocio(ciclomes)
 

    try:
        # Salvar as alterações no banco de dados
        db.session.commit()
        return jsonify({'message': 'CicloMes atualizado com sucesso'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
    
@ciclomes_bp.route('/api/ciclomes/ativar/<int:id>', methods=['PUT'])
@jwt_required()
def ativar_ciclomes(id):
    usuario_id_logado = get_jwt_identity()
    usuario = Usuario.query.get_or_404(usuario_id_logado)

    # Somente administradores podem ativar um CicloMes
    if usuario.tipo_usuario != 'admin':
        return jsonify({'erro': 'Você não tem permissão para ativar o CicloMes'}), 403

    # Buscar o novo CicloMes que será ativado
    novo_ciclo = CicloMes.query.get_or_404(id)

    if novo_ciclo.atual:
        return jsonify({'erro': 'Este CicloMes já está atual'}), 400

    try:
        # Desativar o ciclo atual
        ciclo_atual = CicloMes.query.filter_by(atual=True).first()
        if ciclo_atual:
            ciclo_atual.atual = False
        
        # Ativar o novo CicloMes
        novo_ciclo.atual = True

        # Atualizar todas as contas com as novas regras de negócio
        atualizar_todas_contas(novo_ciclo)

        # Salvar as mudanças no banco de dados
        db.session.commit()

        return jsonify({'message': 'CicloMes ativado e contas atualizadas com sucesso'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
    
@ciclomes_bp.route('/api/ciclomes/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_ciclomes(id):
    usuario_id_logado = get_jwt_identity()
    usuario = Usuario.query.get_or_404(usuario_id_logado)

    # Somente administradores podem ativar um CicloMes
    if usuario.tipo_usuario != 'admin':
        return jsonify({'erro': 'Você não tem permissão para remover um CicloMes'}), 403
    
    ciclomes = CicloMes.query.get(id)
    
    try:
        db.session.delete(ciclomes)
        db.session.commit()
        return jsonify({'message': 'Ciclomes excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
    
@ciclomes_bp.route('/api/ciclomes', methods=['GET'])
@jwt_required()
def get_all_ciclomes():
    ciclomeses = CicloMes.query.all()
    
    return jsonify([{
        'id': ciclomes.id,
        'nome': ciclomes.nome,
        'ano': ciclomes.ano,
        'investimento': ciclomes.investimento,
        'dias': ciclomes.dias,
        'shark': ciclomes.shark,
        'alcancado': ciclomes.alcancado,
        'projecao': ciclomes.projecao,
        'porcentagem_alcancado': ciclomes.porcentagem_alcancado,
        'valor_liquido': ciclomes.valor_liquido,
        'atual' : ciclomes.atual
    } for ciclomes in ciclomeses]),200
    
        
