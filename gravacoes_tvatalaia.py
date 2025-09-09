from flask import Flask
from extensions import db, migrate
from api.routes.Rotas import gravacaoBp

def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__)
    app.secret_key = 'super_secret_key'

    # Configuração do Banco de Dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/db_aeroporto'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Associa o objeto 'db' à nossa aplicação.
    # Isto é feito aqui para evitar a importação circular.
    db.init_app(app)

    #Cria a migração do banco
    migrate.init_app(app, db)

    # Regista o Blueprint com as rotas
    app.register_blueprint(gravacaoBp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000)