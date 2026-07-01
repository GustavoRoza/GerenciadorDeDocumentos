import os
import google.generativeai as genai
from dotenv import load_dotenv
from minio import Minio

load_dotenv()

# --- Configuração Gemini ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erro de configuração Crítico: GEMINI_API_KEY ausente no .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- Configuração MinIO ---
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "127.0.0.1:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
NOME_DO_BUCKET = "documentos"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False # Sem HTTPS localmente
)

# Cria o bucket automaticamente se ele ainda não existir
if not minio_client.bucket_exists(NOME_DO_BUCKET):
    minio_client.make_bucket(NOME_DO_BUCKET)


# Mudança: Adicionamos 'nome_arquivo_minio' para receber o ID correto do main.py
async def gerar_resumo(caminho_arquivo: str, nome_arquivo_minio: str) -> str:
    """
    Faz upload do PDF para o MinIO, processa no Gemini e retorna uma string formatada.
    """
    if not os.path.exists(caminho_arquivo):
        return "Erro: Arquivo não encontrado no servidor."

    try:
        # 1. Salvar no MinIO usando o NOME EXATO que o main.py vai salvar no banco
        minio_client.fput_object(
            NOME_DO_BUCKET,
            nome_arquivo_minio,
            caminho_arquivo,
            content_type="application/pdf"
        )

        # 2. Processamento normal da IA
        arquivo_gemini = genai.upload_file(path=caminho_arquivo, mime_type="application/pdf")

        prompt = (
            "Você é um assistente do sistema Gerenciador de Documentos. "
            "Crie um resumo claro, de no máximo 500 caracteres, objetivo e em texto puro (sem tópicos) para este documento."
        )

        response = model.generate_content([prompt, arquivo_gemini])
        resumo_gerado = response.text

        # 3. Limpeza do Google
        genai.delete_file(arquivo_gemini.name)

        return resumo_gerado

    except Exception as e:
        return f"Indisponibilidade no processamento: {str(e)}"