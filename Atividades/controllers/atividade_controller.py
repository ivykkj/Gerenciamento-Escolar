from flask import request, jsonify, Blueprint
from models.atividade import Atividade
from models import db
from datetime import datetime
import requests

GERENCIAMENTO_API_URL = "http://gerenciamento-svc:8080/api"

atividade_bp = Blueprint('atividade_bp', __name__)

@atividade_bp.route('/atividades', methods=['POST'])
def create_atividade():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400
    
    try:
        turma_id = data['turma_id']
        professor_id = data['professor_id']

        try:
            response = requests.get(f"{GERENCIAMENTO_API_URL}/turmas/{turma_id}")

            if response.status_code == 404:
                return jsonify({"erro": f"Turma com id {turma_id} não encontrado no serviço de Gerenciamento."}), 404

            response.raise_for_status()

        except requests.exceptions.ConnectionError:
            return jsonify({"erro": "Não foi possível conectar ao serviço de Gerenciamento"}), 503

        try:
            response = requests.get(f"{GERENCIAMENTO_API_URL}/professores/{professor_id}")

            if response.status_code == 404:
                return jsonify({"erro": f"Professor com id {professor_id} não encontrado no serviço de Gerenciamento."}), 404

            response.raise_for_status()

        except requests.exceptions.ConnectionError:
            return jsonify({"erro": "Não foi possível conectar ao serviço de Gerenciamento"}), 503        

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
        if 'turma_id' in data:
            turma_id_nova = data['turma_id']
            
            if turma_id_nova != atividade.turma_id:
                try:
                    response = requests.get(f"{GERENCIAMENTO_API_URL}/turmas/{turma_id_nova}")

                    if response.status_code == 404:
                        return jsonify({"erro": f"Nova turma com id {turma_id_nova} não encontrada no Gerenciamento."}), 404

                    response.raise_for_status()
                    
                    atividade.turma_id = turma_id_nova

                except requests.exceptions.ConnectionError:
                    return jsonify({"erro": "Não foi possível conectar ao serviço de Gerenciamento"}), 503
                
        if 'professor_id' in data:
            professor_id_novo = data['professor_id']
            
            if professor_id_novo != atividade.professor_id:
                try:
                    response = requests.get(f"{GERENCIAMENTO_API_URL}/professores/{professor_id_novo}")

                    if response.status_code == 404:
                        return jsonify({"erro": f"Novo professor(a) com id {professor_id_novo} não encontrado(a) no Gerenciamento."}), 404

                    response.raise_for_status()
                    
                    atividade.professor_id = professor_id_novo

                except requests.exceptions.ConnectionError:
                    return jsonify({"erro": "Não foi possível conectar ao serviço de Gerenciamento"}), 503
                
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
    return jsonify(atividade.to_dict()),200

@atividade_bp.route('/atividades/<int:id>', methods=['DELETE'])
def delete_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    
    db.session.delete(atividade)
    db.session.commit()

    return '', 204