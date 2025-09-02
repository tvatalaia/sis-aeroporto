from gravacoes_tvatalaia import create_app
from extensions import db  # Importe o db de extensions.py
from api.models.Models import GravacaoFuncionario
from api.repository.GravacaoRepository import *

# Crie a aplicação para estabelecer o contexto e ler as configurações
app = create_app()

# Use o contexto da aplicação
with app.app_context():
    gravacao = findById(20)

    for funcionario in gravacao.funcionarios_associados:
        print(f"Nome: {funcionario.funcionario.nome} \nFunção: {funcionario.funcao}")
