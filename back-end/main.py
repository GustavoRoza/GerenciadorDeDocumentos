import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from services.ai_service import gerar_resumo
from fastapi.middleware.cors import CORSMiddleware
from services.document_service import buscar_documentos_no_banco, buscar_estatisticas_tipos

# banco

from sqlalchemy.orm import Session

import uuid
from database import get_db, engine
import models
from services.ai_service import gerar_resumo
from fastapi.middleware.cors import CORSMiddleware

# Cria as tabelas automaticamente se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origens_permitidas = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")

    # 1. Gerar o UUID único para o arquivo
    documento_id = uuid.uuid4()

    nome_arquivo_minio = f"{documento_id}.pdf"
    
    temp_path = f"temp_{file.filename}"

    # Salva localmente para processamento
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Pegar o tamanho em bytes do arquivo salvo
    tamanho_arquivo = os.path.getsize(temp_path)

    try:
        # Chama a função isolada no arquivo de serviço
        # resumo = await gerar_resumo(temp_path)
        resumo = await gerar_resumo(temp_path, nome_arquivo_minio)
        # resumo = "Texto de teste: Resumo sem IA"

        # 3. Salvar no PostgreSQL
        novo_documento = models.Documento(
            id=documento_id,
            nome_original=file.filename,
            resumo_ia=resumo,
            mimetype=file.content_type,
            tamanho=tamanho_arquivo
        )

        db.add(novo_documento)
        db.commit()
        db.refresh(novo_documento)

        # Print no terminal do backend conforme solicitado
        print("\n" + "=" * 40)
        print(f"🔍 NOME DO ARQUIVO NO BANCO: {novo_documento.nome_original}")
        print(f"🔍 ARQUIVO SALVO NO BANCO COM ID: {novo_documento.id}")
        print(f"🔍 ID TEMP: {temp_path}")
        print("-" * 40 + "RESUMO NO BANCO" + "-" * 40)
        print(novo_documento.resumo_ia)
        print("=" * 40 + "\n")

        return JSONResponse(
            status_code=201,
            content={
                "id": str(novo_documento.id),
                "filename": novo_documento.nome_original,
                "analise": novo_documento.resumo_ia
            }
        )

    except Exception as e:
        # Se der erro na IA ou no Banco, desfaz qualquer transação
        db.rollback()

        print(f"❌ ERRO DO BACKEND: {str(e)}")

        erro_msg = str(e)
        if "429" in erro_msg or "RESOURCE_EXHAUSTED" in erro_msg:
            raise HTTPException(status_code=429,
                                detail="O servidor de Inteligência Artificial está ocupado no momento. Aguarde um minuto e tente novamente.")

        # Erro genérico
        raise HTTPException(status_code=500, detail="Erro interno ao processar documento.")
    finally:
        # Garante a remoção do arquivo temporário independente de sucesso ou erro
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/documentos/buscar")
async def buscar_documentos(q: str = "", db: Session = Depends(get_db)):
    """
    Endpoint para buscar documentos. 
    A lógica pesada foi movida para services/document_service.py
    """
    try:
        # Chama a função isolada no arquivo de serviço
        resultado = buscar_documentos_no_banco(q, db)
        return resultado
        
    except Exception as e:
        print(f"❌ Erro ao buscar documentos: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao realizar a busca.")

@app.get("/documentos/estatisticas")
async def estatisticas_documentos(db: Session = Depends(get_db)):
    """ Endpoint para retornar a contagem de arquivos por tipo. """
    try:
        resultado = buscar_estatisticas_tipos(db)
        return resultado
    except Exception as e:
        print(f"❌ Erro ao buscar estatísticas: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar estatísticas.")