import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Inicializa o cliente uma única vez
client = genai.Client()

async def analisar_documento(file_path: str) -> str:
    try:
        # 1. Upload para o Gemini
        document_file = client.files.upload(file=file_path)

        # 2. Geração do resumo
        prompt = ("Analise este documento e faça um resumo destacando os pontos principais. Quero o resume em texto bruto, sem quebras de linha "
                  "e caracteres especiais.")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[document_file, prompt]
        )

        # 3. Limpeza no Gemini (opcional, dependendo da sua cota)
        client.files.delete(name=document_file.name)

        return response.text
    except Exception as e:
        print(f"❌ Erro no serviço de IA: {str(e)}")
        raise e