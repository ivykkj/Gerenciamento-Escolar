from models import db
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship

class Nota(db.Model):

    __tablename__ = "notas"

    id = db.Column(db.integer, primary_key=True)
    nota_atividade = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False)

    atividade = relationship("Atividade", back_populates="notas")

    def to_dict(self):
        return {
            'id': self.id,
            'nota_atividade': self.nota_atividade,
            'aluno_id': self.aluno_id,
            'atividade_id': self.atividade_id
        }