from flask import request, jsonify, Blueprint
from models.reserva import Reserva
from models import db
from datetime import datetime
import requests

GERENCIAMENTO_API_URL = "http://gerenciamento-svc:8080/api"

reserva_bp = Blueprint('reserva_bp', __name__)

@reserva_bp.route('/reservas', methods=['POST'])
def create_reserva():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400
    
    try:
        turma_id = data['turma_id']

        try:
            response = requests.get(f"{GERENCIAMENTO_API_URL}/turmas/{turma_id}")

            if response.status_code == 404:
                return jsonify({"erro": f"Turma com id {turma_id} não encontrado no serviço de Gerenciamento."}), 404

            response.raise_for_status()

        except requests.exceptions.ConnectionError:
            return jsonify({"erro": "Não foi possível conectar ao serviço de Gerenciamento"}), 503

        nova_reserva = Reserva(
            num_sala = data['num_sala'],
            lab = data['lab'],
            data_reserva = datetime.strptime(data['data_reserva'],'%d/%m/%Y').date(),
            turma_id = data['turma_id']
        )

    except KeyError as e:
        return jsonify({"erro": f"O campo '{e.argd[0]}' é obrigatório."}),400
    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use 'dd/mm/yyyy'."}),400
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro inesperado: {str(e)}"}),500
    
    db.session.add(nova_reserva)
    db.session.commit()
    return jsonify(nova_reserva.to_dict()),201

@reserva_bp.route('/reservas', methods=['GET'])
def get_reservas():
    reservas = Reserva.query.all()
    return jsonify([a.to_dict() for a in reservas])

@reserva_bp.route('/reservas/<int:id>', methods=['GET'])
def get_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    return jsonify(reserva.to_dict())

@reserva_bp.route('/reservas/<int:id>', methods=['PUT'])
def update_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Corpo da requisição não pode ser vazio."}), 400

    try:
        if 'turma_id' in data:
            turma_id_nova = data['turma_id']
            
            if turma_id_nova != reserva.turma_id:
                try:
                    response = requests.get(f"{GERENCIAMENTO_API_URL}/turmas/{turma_id_nova}")

                    if response.status_code == 404:
                        return jsonify({"erro": f"Nova turma com id {turma_id_nova} não encontrada no Gerenciamento."}), 404

                    response.raise_for_status()
                    
                    reserva.turma_id = turma_id_nova

                except requests.exceptions.ConnectionError:
                    return jsonify({"erro": "Não foi possível conectar ao serviço de Gerenciamento"}), 503
                
        reserva.num_sala = data.get('num_sala', reserva.num_sala)
        reserva.lab = data.get('lab', reserva.lab)
        
        if 'data_reserva' in data:
            reserva.data_reserva = datetime.strptime(data['data_reserva'],'%d/%m/%Y').date()

    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use 'dd/mm/yyyy'."}), 400
    except Exception as e:
        return jsonify({"erro": "Ocorreu um erro ao atualizar os dados."}), 500

    db.session.commit()
    return jsonify(reserva.to_dict()),200

@reserva_bp.route('/reservas/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    reserva = Reserva.query.get_or_404(id)

    db.session.delete(reserva)
    db.session.commit()

    return '', 204