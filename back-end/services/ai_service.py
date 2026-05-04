import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Erro de configuração Crítico: GEMINI_API_KEY ausente no .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')


# Agora é async para funcionar com o 'await' do main.py
async def gerar_resumo(caminho_arquivo: str) -> str:
    """
    Faz upload do PDF para a API do Gemini, processa e retorna o resumo.
    """
    if not os.path.exists(caminho_arquivo):
        return "Erro: Arquivo não encontrado no servidor."

    try:
        # 1. Envia o arquivo físico para a IA
        arquivo_gemini = genai.upload_file(path=caminho_arquivo, mime_type="application/pdf")

        prompt = (
            "Você é um assistente do sistema Gerenciador de Documentos. "
            "Crie um resumo claro, objetivo e em texto puro (sem tópicos) para este documento."
        )

        # 2. Gera o conteúdo enviando o prompt e a referência do arquivo
        response = model.generate_content([prompt, arquivo_gemini])
        resumo_gerado = response.text

        # 3. Limpeza: Apaga o documento dos servidores do Google imediatamente após o uso
        genai.delete_file(arquivo_gemini.name)

        return resumo_gerado

    except Exception as e:
        return f"Indisponibilidade no serviço de IA: {str(e)}"