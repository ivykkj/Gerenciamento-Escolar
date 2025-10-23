from models import db
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship

class Aluno(db.Model):
    
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_1_semestre = db.Column(db.Float, nullable=False)
    nota_2_semestre = db.Column(db.Float, nullable=False)
    media_final = db.Column(db.Float, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)

    turma = relationship("Turma", back_populates="alunos")

    def calcular_media(self):
        self.media_final = (self.nota_1_semestre + self.nota_2_semestre) / 2

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'data_nascimento': self.data_nascimento.strftime('%d/%m/%Y'),
            'nota_1_semestre': self.nota_1_semestre,
            'nota_2_semestre': self.nota_2_semestre,
            'media_final': self.media_final,
            'turma_id': self.turma_id
        }