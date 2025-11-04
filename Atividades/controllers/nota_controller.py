from flask import request, jsonify, Blueprint
from models.nota import Nota
from models.atividade import Atividade
from models import db
import requests

#TO DO: comunicação com api de Gerenciamento e a validação síncrona no POST e PUT

nota_bp = Blueprint('nota_bp', __name__)

@nota_bp.route('/notas', methods=['POST'])
def create_nota():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400
    
    try:
        aluno_id = data['aluno_id']

        if not Atividade.query.get(data['atividade_id']):
            return jsonify({'erro': 'Atividade não encontrada'}), 404
        
        nova_nota = Nota(
            nota = data['data'],
            aluno_id = data['aluno_id'],
            atividade_id = data['atividade_id']
        )

    except KeyError as e:
        return jsonify({"erro": f"O campo '{e.argd[0]}' é obrigatório."}),400
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro inesperado: {str(e)}"}),500
    
    db.session.add(nova_nota)
    db.session.commit()
    return jsonify(nova_nota.to_dict()),201

@nota_bp.route('/notas', methods=['GET'])
def get_notas():
    nota = Nota.query.all()
    return jsonify(nota.to_dict())

@nota_bp.route('/notas/<int:id>', methods=['GET'])
def get_nota(id):
    nota = Nota.query.get_or_404(id)
    return jsonify(nota.to_dict())

@nota_bp.route('/notas/<int:id>', methods=['PUT'])
def upsdate_nota(id):
    nota = Nota.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

    try:
        nota.nota = data.get('nota', nota.nota)

        if 'atividade_id' in data:
            atividade = Atividade.query.get(data['atividade_id'])
            if not atividade:
                return jsonify({'message': 'Nova atividade não encontrada'}), 400
            nota.atividade_id = data['atividade_id']

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