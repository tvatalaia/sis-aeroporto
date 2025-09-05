from extensions import db
from sqlalchemy import text
from sqlalchemy.orm import joinedload, selectinload
from api.models.Models import Gravacao, GravacaoFuncionario

def findAll():
    return Gravacao.query.options(
        # Pré-carrega os relacionamentos "um-para-um" (usa JOIN)
        joinedload(Gravacao.programa),
        joinedload(Gravacao.producao_interna),
        joinedload(Gravacao.cliente_externo),
        # Pré-carrega a equipa (relacionamento "muitos-para-muitos")
        # 'selectinload' é mais eficiente aqui, pois faz uma segunda query para todas as equipas.
        selectinload(Gravacao.funcionarios_associados).joinedload(GravacaoFuncionario.funcionario)
    ).order_by(Gravacao.data_hora.desc()).all()

def findById(id: int):
    return Gravacao.query.get(id)

def insert(g : Gravacao):
    db.session.add(g)

def update(g : Gravacao):
    pass

def remove(g : Gravacao):
    db.session.delete(g)