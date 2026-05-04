import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from services.ai_service import analisar_documento
from fastapi.middleware.cors import CORSMiddleware

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
async def upload(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")

    temp_path = f"temp_{file.filename}"

    # Salva localmente para processamento
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Chama a função isolada no arquivo de serviço
        resumo = await analisar_documento(temp_path)

        # Print no terminal do backend conforme solicitado
        print("\n" + "=" * 40)
        print(f"🔍 RESUMO DO ARQUIVO: {file.filename}")
        print("-" * 40)
        print(resumo)
        print("=" * 40 + "\n")

        return JSONResponse(
            status_code=200,
            content={
                "filename": file.filename,
                "analise": resumo
            }
        )
    except Exception as e:
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