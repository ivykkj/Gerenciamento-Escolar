from models import db
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship

class Atividade(db.Model):

    __tablename__ = "atividades"

    id = db.Column(db.integer, primary_key=True)
    nome_atividade = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    peso_porcento = db.Column(db.Integer, nullable=False)
    data_entrega = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)

    notas = relationship("Nota", back_populates="atividades")

    def to_dict(self):
        return{
            'id':self.id,
            'nome_atividade':self.nome_atividade,
            'descricao':self.descricao,
            'peso_porcento':self.peso_porcento,
            'data_entrega':self.data_entrega,
            'turma_id':self.turma_id,
            'professor_id':self.professor_id
        }