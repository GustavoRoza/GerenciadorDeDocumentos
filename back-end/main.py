import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from google import genai

# Carregar variáveis do .env
load_dotenv()

# O novo cliente detecta automaticamente a variável GEMINI_API_KEY do ambiente
client = genai.Client()

app = FastAPI()


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        document_file = client.files.upload(file=temp_path)

        prompt = "Analise este documento e faça um resumo destacando os pontos principais."
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[document_file, prompt]
        )

        # Imprime a resposta no terminal do back-end
        print("\n" + "=" * 40)
        print("🔍 ANÁLISE GERADA PELO GEMINI:")
        print("=" * 40)
        print(response.text)
        print("=" * 40 + "\n")

        client.files.delete(name=document_file.name)
        os.remove(temp_path)

        return JSONResponse(
            status_code=200,
            content={
                "filename": file.filename,
                "analise": response.text
            }
        )
    except Exception as e:
        print(f"❌ ERRO INTERNO: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500,
                            detail="Erro interno ao processar o documento. Verifique os logs do terminal.")