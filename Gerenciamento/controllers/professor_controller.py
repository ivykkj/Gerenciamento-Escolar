from flask import request, jsonify, Blueprint
from models import db
from models.professor import Professor

professor_bp = Blueprint('professor_bp', __name__)

@professor_bp.route('/professores', methods=['POST'])
def create_professor():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

    try:
        novo_professor = Professor(
            nome=data['nome'],
            idade=data['idade'],
            materia=data['materia'],
            observacoes=data.get('observacoes')
        )
    except KeyError as e:
        return jsonify({"erro": f"O campo '{e.args[0]}' é obrigatório."}), 400

    db.session.add(novo_professor)
    db.session.commit()
    return jsonify(novo_professor.to_dict()), 201

@professor_bp.route('/professores', methods=['GET'])
def get_professores():
    professores = Professor.query.all()
    return jsonify([p.to_dict() for p in professores])

@professor_bp.route('/professores/<int:id>', methods=['GET'])
def get_professor(id):
    professor = Professor.query.get_or_404(id)
    return jsonify(professor.to_dict())

@professor_bp.route('/professores/<int:id>', methods=['PUT'])
def update_professor(id):
    professor = Professor.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

    try:
        professor.nome = data.get('nome', professor.nome)
        professor.idade = data.get('idade', professor.idade)
        professor.materia = data.get('materia', professor.materia)
        professor.observacoes = data.get('observacoes', professor.observacoes)
    except Exception as e:
        return jsonify({"erro": "Ocorreu um erro ao atualizar os dados."}), 400

    db.session.commit()
    return jsonify(professor.to_dict())

@professor_bp.route('/professores/<int:id>', methods=['DELETE'])
def delete_professor(id):
    professor = Professor.query.get_or_404(id)
    db.session.delete(professor)
    db.session.commit()
    return '', 204