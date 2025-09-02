from gravacoes_tvatalaia import create_app
from extensions import db
from api.models.Models import GravacaoFuncionario # Importe o modelo

# Crie a aplicação para estabelecer o contexto
app = create_app()

# Use o contexto da aplicação
with app.app_context():
    print("="*60)
    print("INICIANDO PROCESSO DE SINCRONIZAÇÃO DE TABELA...")
    print("="*60)
    
    tabela_para_recriar = GravacaoFuncionario.__table__
    
    print(f"A tentar apagar a tabela '{tabela_para_recriar.name}'...")
    try:
        # Apaga a tabela da base de dados
        tabela_para_recriar.drop(db.engine)
        print("Tabela apagada com sucesso.")
    except Exception as e:
        print(f"Aviso: Não foi possível apagar a tabela (pode já não existir). Erro: {e}")

    print(f"\nA tentar criar a tabela '{tabela_para_recriar.name}' com base no Model...")
    try:
        # Cria a tabela novamente, usando a definição exata do seu models.py
        tabela_para_recriar.create(db.engine)
        print("TABELA CRIADA COM SUCESSO!")
        print("A estrutura da base de dados está agora 100% sincronizada com o seu código.")
    except Exception as e:
        print(f"ERRO CRÍTICO: Não foi possível criar a tabela. Erro: {e}")

    print("\n="*60)
    print("PROCESSO CONCLUÍDO.")
    print("="*60)