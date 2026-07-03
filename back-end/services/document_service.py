import os
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from minio import Minio
from dotenv import load_dotenv
import models
from services.ai_service import gerar_vetor_pesquisa

load_dotenv()

# --- Configuração MinIO ---
# Importamos as configurações para gerar a URL temporária
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "127.0.0.1:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
NOME_DO_BUCKET = "documentos"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False # Use True em produção se usar HTTPS
)


def buscar_documentos_no_banco(q: str, db: Session):
    """
    Realiza a busca usando pgvector.
    Se a IA falhar, faz o fallback para a busca clássica.
    """
    query = db.query(models.Documento)
    
    if q:
        vetor_pergunta = gerar_vetor_pesquisa(q)
        if vetor_pergunta:
            distancia = models.Documento.vetor_resumo.cosine_distance(vetor_pergunta)
            
            # A TRAVA DE SEGURANÇA: 
            # O documento SÓ aparece se tiver a palavra exata (ilike)
            # OU se a IA tiver certeza altíssima do contexto (distância < 0.38).
            # Qualquer coisa diferente disso é bloqueada e não aparece na tela.
            query = query.filter(
                (models.Documento.nome_original.ilike(f"%{q}%")) |
                (models.Documento.resumo_ia.ilike(f"%{q}%")) |
                (distancia < 0.38)
            ).order_by(distancia)
        else:
            query = query.filter(
                (models.Documento.resumo_ia.ilike(f"%{q}%")) |
                (models.Documento.nome_original.ilike(f"%{q}%"))
            )
    else:
        query = query.order_by(models.Documento.data_criacao.desc())
        
    # Como o filtro agora é rigoroso, podemos usar o .all() normal.
    # Só vai retornar o que realmente tem a ver.
    documentos = query.all()
    
    # Formatando o resultado para evitar erro de conversão de UUID e Datas no JSON
    resultado = []
    for doc in documentos:
        # 1. Recria o nome exato do arquivo salvo no MinIO
        nome_arquivo_minio = f"{str(doc.id)}.pdf"
        
        # 2. Gera a URL temporária válida por 3 minutos
        try:
            url_download = minio_client.presigned_get_object(
                bucket_name=NOME_DO_BUCKET,
                object_name=nome_arquivo_minio,
                expires=timedelta(minutes=3)
            )
        except Exception as e:
            print(f"❌ Erro ao gerar link do MinIO para {nome_arquivo_minio}: {e}")
            url_download = None

        resultado.append({
            "id": str(doc.id),
            "nome_original": doc.nome_original,
            "resumo_ia": doc.resumo_ia,
            "mimetype": doc.mimetype,
            "tamanho": doc.tamanho,
            "data_criacao": doc.data_criacao.isoformat() if doc.data_criacao else None,
            "url_download": url_download  # Novo campo retornado para a API
        })
        
    return resultado


def buscar_estatisticas_tipos(db: Session):
    """
    Agrupa os documentos por mimetype e conta quantos de cada tipo existem.
    """
    resultados = db.query(
        models.Documento.mimetype,
        func.count(models.Documento.id).label('quantidade')
    ).group_by(models.Documento.mimetype).all()
    
    return [{"tipo": r.mimetype, "quantidade": r.quantidade} for r in resultados]

def deletar_documento(documento_id: str, db: Session):
    #busca o pdf no banco pra ver se ele existe
    doc = db.query(models.Documento).filter(models.Documento.id == documento_id).first()
    
    if not doc:
        return False

    nome_arquivo_minio = f"{str(doc.id)}.pdf"

    # deleta o PDF do MinIO
    try:
        minio_client.remove_object(NOME_DO_BUCKET, nome_arquivo_minio)
        print(f"🗑️ Arquivo {nome_arquivo_minio} removido do MinIO.")
    except Exception as e:
        print(f"⚠️ Aviso: Erro ao deletar do MinIO (pode já ter sido apagado): {e}")

    # seleta do banco
    db.delete(doc)
    db.commit()
    print(f"🗑️ Registro {documento_id} removido do Banco de Dados.")
    
    return True

