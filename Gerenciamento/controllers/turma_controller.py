from flask import request, jsonify, Blueprint
from models import db
from models.turma import Turma
from models.professor import Professor

turma_bp = Blueprint('turma_bp', __name__)

@turma_bp.route('/turmas', methods=['POST'])
def create_turma():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

    try:
        professor = Professor.query.get(data['professor_id'])
        if not professor:
            return jsonify({'message': 'Professor não encontrado'}), 400

        nova_turma = Turma(
            descricao=data['descricao'],
            ativo=data.get('ativo', True),
            professor_id=data['professor_id']
        )
    except KeyError as e:
        return jsonify({"erro": f"O campo '{e.args[0]}' é obrigatório."}), 400
    
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify(nova_turma.to_dict()), 201

@turma_bp.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = Turma.query.all()
    return jsonify([t.to_dict() for t in turmas])

@turma_bp.route('/turmas/<int:id>', methods=['GET'])
def get_turma(id):
    turma = Turma.query.get_or_404(id)
    return jsonify(turma.to_dict())

@turma_bp.route('/turmas/<int:id>', methods=['PUT'])
def update_turma(id):
    turma = Turma.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400
    
    try:
    
        turma.descricao = data.get('descricao', turma.descricao)
        turma.ativo = data.get('ativo', turma.ativo)

        if 'professor_id' in data:
            professor = Professor.query.get(data['professor_id'])
            if not professor:
                return jsonify({'message': 'Novo professor não encontrado'}), 400
            turma.professor_id = data['professor_id']
    except Exception as e:
        return jsonify({"erro": "Ocorreu um erro ao atualizar os dados."}), 400
        
    db.session.commit()
    return jsonify(turma.to_dict())

@turma_bp.route('/turmas/<int:id>', methods=['DELETE'])
def delete_turma(id):
    turma = Turma.query.get_or_404(id)
    db.session.delete(turma)
    db.session.commit()
    return '', 204