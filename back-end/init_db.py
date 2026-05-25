import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# carregamento do .env (la tem os dados do banco)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ Erro: DATABASE_URL não encontrada no arquivo .env")


def clonar_e_criar_banco():
    try:
        url_base, banco_nome = DATABASE_URL.rsplit("/", 1)
    except ValueError:
        print("❌ Erro: Formato da DATABASE_URL no .env é inválido.")
        return

    url_postgres_padrao = f"{url_base}/postgres"

    # Cria engine temporário no banco 'postgres' padrão para criar o banco do projeto
    engine_servidor = create_engine(url_postgres_padrao, isolation_level="AUTOCOMMIT")

    with engine_servidor.connect() as conexao:
        # Verifica se o banco existe
        query = text("SELECT 1 FROM pg_database WHERE datname = :dbname")
        banco_existe = conexao.execute(query, {"dbname": banco_nome}).scalar()

        if not banco_existe:
            print(f"❌ Banco de dados '{banco_nome}' não foi encontrado.")
            print(f"Criando o banco '{banco_nome}'...")
            conexao.execute(text(f'CREATE DATABASE "{banco_nome}"'))
            print(f"✅ Banco de dados '{banco_nome}' criado com sucesso!")
        else:
            print(f"✅ O banco de dados '{banco_nome}' já existe.")

    engine_servidor.dispose()

    try:
        from database import engine
        import models

        # Executa o mapeamento do SQLAlchemy para gerar as tabelas físicas
        models.Base.metadata.create_all(bind=engine)
        print("✅ Estrutura do banco sincronizada!")
    except Exception as e:
        print(f"❌ Erro ao criar as tabelas do modelo: {str(e)}")


if __name__ == "__main__":
    print("==================================================")
    print("CRIAÇÃO DO BANCO DE DADOS")
    print("==================================================")
    clonar_e_criar_banco()
    print("==================================================")