from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#                                     //usuario:senha@localhost:5432/nome_do_banco
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1F16EBD3@localhost:5432/gerenciador_documentos"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para as rotas do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()