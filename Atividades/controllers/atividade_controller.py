from flask import request, jsonify, Blueprint
from models.atividade import Atividade
from models import db
from datetime import datetime
import requests

#TO DO: comunicação com api de Gerenciamento e a validação síncrona no POST e PUT

atividade_bp = Blueprint('atividade_bp', __name__)

@atividade_bp.route('/atividades', methods=['POST'])
def create_atividade():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400
    
    try:
        turma_id = data['turma_id']
        professor_id = data['professor_id']

        nova_atividade = Atividade(
            nome_atividade = data['nome_atividade'],
            descricao = data['descricao'],
            peso_porcento = data['peso_porcento'],
            data_entrega = datetime.strptime(data['data_entrega'],'%d/%m/%Y').date(),
            turma_id = data['turma_id'],
            professor_id = data['professor_id']
        )
    
    except KeyError as e:
        return jsonify({"erro": f"O campo '{e.argd[0]}' é obrigatório."}),400
    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use 'dd/mm/yyyy'."}),400
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro inesperado: {str(e)}"}),500
    
    db.session.add(nova_atividade)
    db.session.commit()
    return jsonify(nova_atividade.to_dict()),201

@atividade_bp.route('/atividades', methods=['GET'])
def get_atividades():
    atividades = Atividade.query.all()
    return jsonify([a.to_dict() for a in atividades])

@atividade_bp.route('/atividades/<int:id>', methods=['GET'])
def get_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    return jsonify(atividade.to_dict())

@atividade_bp.route('/atividades/<int:id>', methods=['PUT'])
def update_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

    try:
        atividade.nome_atividade = data.get('nome_atividade', atividade.nome_atividade)
        atividade.descricao = data.get('descricao', atividade.descricao)
        atividade.peso_porcento = data.get('peso_porcento', atividade.peso_porcento)

        if 'data_entrega' in data:
            atividade.data_entrega = datetime.strptime(data['data_entrega'],'%d/%m/%Y').date()

    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use 'dd/mm/yyyy'."}), 400
    except Exception as e:
        return jsonify({"erro": "Ocorreu um erro ao atualizar os dados."}), 500

    db.session.commit()
    return jsonify(atividade.to_dict()),201

@atividade_bp.route('/atividades/<int:id>', methods=['DELETE'])
def delete_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    
    db.session.delete(atividade)
    db.session.commit()

    return '', 204