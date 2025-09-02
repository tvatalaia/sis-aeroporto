from extensions import db
from sqlalchemy import text
from api.models.Models import Gravacao

def findAll():
    sql = text("select g.id_gravacao as id, g.data_hora, g.tipo, p.descricao from gravacao g " \
    "left join programa p on p.id_programa = g.fk_id_programa where tipo = 'Ao Vivo' " \
    "UNION " \
    "select g.id_gravacao as id, g.data_hora, g.tipo, pi.descricao from gravacao g " \
    "left join producao_interna pi on pi.id_producao_interna = g.fk_id_producao_interna where tipo in('Interna') " \
    "UNION " \
    "select g.id_gravacao as id, g.data_hora, g.tipo, ce.descricao from gravacao g " \
    "left join cliente_externo ce on ce.id_cliente_externo = g.fk_id_cliente_externo where tipo in('Externa');")

    return db.session.execute(sql).fetchall()

def findById(id: int):
    ### gravacoes = findAll()

    #for gravacao in gravacoes:
    #    if gravacao[0] == id:
    #        gravacaoObj = Gravacao(
    #            id_gravacao = gravacao[0],
    #            id_gravacao = gravacao[0],
#                id_gravacao = gravacao[0],
 #               id_gravacao = gravacao[0]
  #          )
    
    return Gravacao.query.get(id)

def carregar_equipe(id: int):
    sql = text("select f.nome, gf.funcao from gravacao g " \
    "left join gravacao_funcionario gf on gf.fk_id_gravacao = g.id_gravacao " \
    "inner join funcionario f on f.id_funcionario = gf.fk_id_funcionario " \
    "where g.id_gravacao = {id};")

def insert(g : Gravacao):
    db.session.add(g)

def update(g : Gravacao):
    pass

def remove(g : Gravacao):
    db.session.delete(g)