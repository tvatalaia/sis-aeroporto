from datetime import datetime

from flask import json
from api.repository.GravacaoRepository import *
from api.models.Models import Gravacao, GravacaoFuncionario
from extensions import db

def carregar_gravacoes():
    return findAll()

def carregar_gravacao(id: int):
    return findById(id)

def inserir_gravacao(data):    
    try:
        d = datetime.strptime(data.get("data"), "%Y-%m-%d").date()
        t = datetime.strptime(data.get("horario"), "%H:%M").time()
        timestamp = datetime.combine(d, t)
        
        nova_gravacao = Gravacao(
            data_hora=timestamp,
            tipo=data.get("tipo")
        )

        tipo = data.get("tipo")
        equipe_json_string = None

        if tipo == 'Ao Vivo':
            nova_gravacao.fk_id_programa = int(data.get("programa"))
        elif tipo == 'Interna':
            nova_gravacao.fk_id_producao_interna = int(data.get("producao_interna"))
            equipe_json_string = data.get("equipe_data_interna")
        else:
            nova_gravacao.fk_id_cliente_externo = int(data.get("cliente_externo"))
            equipe_json_string = data.get("equipe_data_externa")

        # Adiciona a gravação à sessão e obtem o ID
        db.session.add(nova_gravacao)
        db.session.flush()

        id_da_nova_gravacao = nova_gravacao.id_gravacao

        # Cria os objetos de equipe
        if equipe_json_string:
            equipe_lista = json.loads(equipe_json_string)
            for membro in equipe_lista:
                
                # --- A CORREÇÃO ESTÁ AQUI ---
                # Em vez de atribuir o ID, atribuímos o objeto 'nova_gravacao' inteiro
                # ao relacionamento 'gravacao'.
                novo_membro_equipe = GravacaoFuncionario(
                    fk_id_gravacao = id_da_nova_gravacao,  # <--- Atribui o objeto pai
                    fk_id_funcionario = int(membro["id"]),
                    funcao=membro["funcao"]
                )
                db.session.add(novo_membro_equipe)

        # --- 4. Finalizar a Transação ---
        # Apenas um commit no final para salvar tudo de uma vez.
        db.session.commit()
        
        return {"success": True, "message": "Gravação e equipe inseridas com sucesso."}

    except Exception as e:
        # Se qualquer passo falhar, desfaz tudo
        print("ERRO NO SERVICE: A transação foi revertida.")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem do erro: {e}")
        db.session.rollback()
        return {"success": False, "message": f"Ocorreu um erro: {e}"}

#OBS: Tratar a data. Vai vir como texto
def atualizarGravacao(id: int):
    pass