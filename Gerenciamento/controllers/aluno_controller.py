from flask import request, jsonify, Blueprint
from models import db
from models.aluno import Aluno
from models.turma import Turma
from datetime import datetime

aluno_bp = Blueprint('aluno_bp', __name__)

@aluno_bp.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

    try:
        if not Turma.query.get(data['turma_id']):
            return jsonify({'erro': 'Turma não encontrada'}), 404

        novo_aluno = Aluno(
            nome=data['nome'],
            idade=data['idade'],
            data_nascimento=datetime.strptime(data['data_nascimento'], '%d/%m/%Y').date(),
            nota_1_semestre=data['nota_1_semestre'],
            nota_2_semestre=data['nota_2_semestre'],
            turma_id=data['turma_id']
        )
        novo_aluno.calcular_media()

    except KeyError as e:
        return jsonify({"erro": f"O campo '{e.args[0]}' é obrigatório."}), 400
    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use 'dd/mm/yyyy'."}), 400

    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify(novo_aluno.to_dict()), 201

@aluno_bp.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    return jsonify([a.to_dict() for a in alunos])

@aluno_bp.route('/alunos/<int:id>', methods=['GET'])
def get_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    return jsonify(aluno.to_dict())

@aluno_bp.route('/alunos/<int:id>', methods=['PUT'])
def update_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

    try:
        aluno.nome = data.get('nome', aluno.nome)
        aluno.idade = data.get('idade', aluno.idade)
        aluno.nota_1_semestre = data.get('nota_1_semestre', aluno.nota_1_semestre)
        aluno.nota_2_semestre = data.get('nota_2_semestre', aluno.nota_2_semestre)

        if 'data_nascimento' in data:
            aluno.data_nascimento = datetime.strptime(data['data_nascimento'], '%d/%m/%Y').date()

        if 'turma_id' in data:
            turma = Turma.query.get(data['turma_id'])
            if not turma:
                return jsonify({'message': 'Nova turma não encontrada'}), 400
            aluno.turma_id = data['turma_id']
            
        aluno.calcular_media_final()

    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use 'dd/mm/yyyy'."}), 400
    except Exception as e:
        return jsonify({"erro": "Ocorreu um erro ao atualizar os dados."}), 500

    
    db.session.commit()
    return jsonify(aluno.to_dict())

@aluno_bp.route('/alunos/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return '', 204