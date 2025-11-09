from flask import request, jsonify, Blueprint
from models.nota import Nota
from models.atividade import Atividade
from models import db
import requests

GERENCIAMENTO_API_URL = "http://gerenciamento-svc:8080/api"

nota_bp = Blueprint('nota_bp', __name__)

@nota_bp.route('/notas', methods=['POST'])
def create_nota():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400
    
    try:
        aluno_id = data['aluno_id']

        try:
            response = requests.get(f"{GERENCIAMENTO_API_URL}/alunos/{aluno_id}")

            if response.status_code == 404:
                return jsonify({"erro": f"Aluno(a) com id {aluno_id} não encontrado no serviço de Gerenciamento."}), 404

            response.raise_for_status()

        except requests.exceptions.ConnectionError:
            return jsonify({"erro": "Não foi possível conectar ao serviço de Gerenciamento"}), 503

        if not Atividade.query.get(data['atividade_id']):
            return jsonify({'erro': 'Atividade não encontrada'}), 404
        
        nova_nota = Nota(
            nota_atividade = data['nota_atividade'],
            aluno_id = data['aluno_id'],
            atividade_id = data['atividade_id']
        )

    except KeyError as e:
        return jsonify({"erro": f"O campo '{e.args[0]}' é obrigatório."}),400
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro inesperado: {str(e)}"}),500
    
    db.session.add(nova_nota)
    db.session.commit()
    return jsonify(nova_nota.to_dict()),201

@nota_bp.route('/notas', methods=['GET'])
def get_notas():
    notas = Nota.query.all()
    return jsonify([n.to_dict() for n in notas])

@nota_bp.route('/notas/<int:id>', methods=['GET'])
def get_nota(id):
    nota = Nota.query.get_or_404(id)
    return jsonify(nota.to_dict())

@nota_bp.route('/notas/<int:id>', methods=['PUT'])
def update_nota(id):
    nota = Nota.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

    try:
        if 'aluno_id' in data:
            aluno_id_novo = data['aluno_id']
            
            if aluno_id_novo != nota.aluno_id:
                try:
                    response = requests.get(f"{GERENCIAMENTO_API_URL}/alunos/{aluno_id_novo}")

                    if response.status_code == 404:
                        return jsonify({"erro": f"Novo(a) aluno(a) com id {aluno_id_novo} não encontrada no Gerenciamento."}), 404

                    response.raise_for_status()
                    
                    nota.aluno_id = aluno_id_novo

                except requests.exceptions.ConnectionError:
                    return jsonify({"erro": "Não foi possível conectar ao serviço de Gerenciamento"}), 503
        
        if 'atividade_id' in data:
            atividade = Atividade.query.get(data['atividade_id'])
            if not atividade:
                return jsonify({'message': 'Nova atividade não encontrada'}), 400
            nota.atividade_id = data['atividade_id']

        nota.nota_atividade = data.get('nota_atividade', nota.nota_atividade)

    except Exception as e:
        return jsonify({"erro": "Ocorreu um erro ao atualizar os dados."}), 500
    
    db.session.commit()
    return jsonify(nota.to_dict())

@nota_bp.route('/notas/<int:id>', methods=['DELETE'])
def delete_nota(id):
    nota = Nota.query.get_or_404(id)

    db.session.delete(nota)
    db.session.commit()

    return '', 204    