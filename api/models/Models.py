from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from extensions import db

class ClienteExterno(db.Model):
    __tablename__ = 'cliente_externo'
    id_cliente_externo = db.Column(Integer, primary_key=True)
    descricao = db.Column(String(50), nullable=False)
    
    # Relacionamento: Um cliente externo pode ter várias gravações
    gravacoes = relationship('Gravacao', back_populates='cliente_externo')

class Departamento(db.Model):
    __tablename__ = 'departamento'
    id_departamento = db.Column(Integer, primary_key=True)
    descricao = db.Column(String(50), nullable=False)

    # Relacionamento: Um departamento pode ter vários funcionários
    funcionarios = relationship('Funcionario', back_populates='departamento')

class ProducaoInterna(db.Model):
    __tablename__ = 'producao_interna'
    id_producao_interna = db.Column(Integer, primary_key=True)
    descricao = db.Column(String(50), nullable=False)

    # Relacionamento: Uma produção interna pode ter várias gravações
    gravacoes = relationship('Gravacao', back_populates='producao_interna')

class Programa(db.Model):
    __tablename__ = 'programa'
    id_programa = db.Column(Integer, primary_key=True)
    descricao = db.Column(String(50), nullable=False)

    # Relacionamento: Um programa pode ter várias gravações
    gravacoes = relationship('Gravacao', back_populates='programa')

class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    id_funcionario = db.Column(Integer, primary_key=True)
    nome = db.Column(String(150), nullable=False)
    fk_id_departamento = db.Column(Integer, ForeignKey('departamento.id_departamento', ondelete='RESTRICT'))

    # Relacionamento: Um funcionário pertence a um departamento
    departamento = relationship('Departamento', back_populates='funcionarios')

    # Relacionamento com a tabela de associação
    gravacoes_associadas = relationship('GravacaoFuncionario', back_populates='funcionario')

class Gravacao(db.Model):
    __tablename__ = 'gravacao'
    id_gravacao = db.Column(Integer, primary_key=True)
    data_hora = db.Column(TIMESTAMP, nullable=False)
    data_hora_modificacao = db.Column(TIMESTAMP, nullable=True)
    tipo = db.Column(Enum('Ao Vivo', 'Interna', 'Externa'), nullable=False)
    
    # Chaves Estrangeiras
    fk_id_programa = db.Column(Integer, ForeignKey('programa.id_programa', ondelete='CASCADE'))
    fk_id_producao_interna = db.Column(Integer, ForeignKey('producao_interna.id_producao_interna', ondelete='CASCADE'))
    fk_id_cliente_externo = db.Column(Integer, ForeignKey('cliente_externo.id_cliente_externo', ondelete='CASCADE'))

    # Relacionamentos para aceder aos objetos diretamente
    programa = relationship('Programa', back_populates='gravacoes')
    producao_interna = relationship('ProducaoInterna', back_populates='gravacoes')
    cliente_externo = relationship('ClienteExterno', back_populates='gravacoes')

    # Relacionamento com a tabela de associação
    funcionarios_associados = relationship('GravacaoFuncionario', back_populates='gravacao')

    # Adiciona a regra de verificação (CheckConstraint) ao modelo
    __table_args__ = (
        CheckConstraint(
            "((tipo = 'Ao Vivo' AND fk_id_programa IS NOT NULL AND fk_id_producao_interna IS NULL AND fk_id_cliente_externo IS NULL) OR "
            "(tipo = 'Interna' AND fk_id_programa IS NULL AND fk_id_producao_interna IS NOT NULL AND fk_id_cliente_externo IS NULL) OR "
            "(tipo = 'Externa' AND fk_id_programa IS NULL AND fk_id_producao_interna IS NULL AND fk_id_cliente_externo IS NOT NULL))",
            name='chk_tipo_gravacao_exclusivo'
        ),
    )

class GravacaoFuncionario(db.Model):
    __tablename__ = 'gravacao_funcionario'
    # Chaves primárias compostas
    id_gravacao_funcionario = db.Column(Integer, primary_key=True)
    fk_id_gravacao = db.Column(Integer, ForeignKey('gravacao.id_gravacao', ondelete='RESTRICT'))
    fk_id_funcionario = db.Column(Integer, ForeignKey('funcionario.id_funcionario', ondelete='SET NULL'))
    
    # Coluna de dados extra
    funcao = db.Column(String(50), nullable=False)

    # Relacionamentos para navegar a partir desta classe
    gravacao = relationship('Gravacao', back_populates='funcionarios_associados')
    funcionario = relationship('Funcionario', back_populates='gravacoes_associadas')

    __table_args__ = (db.UniqueConstraint('fk_id_gravacao', 'fk_id_funcionario', name='uc_gravacao_funcionario'), )