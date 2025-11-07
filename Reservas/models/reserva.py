from models import db
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship

class Reserva(db.Model):

    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer, nullable=False)
    lab = db.Column(db.Boolean, nullable=False)
    data_reserva = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return{
            'id':self.id,
            'num_sala':self.num_sala,
            'lab':self.lab,
            'data_reserva':self.data_reserva,
            'turma_id':self.turma_id
        }