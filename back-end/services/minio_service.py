# services/minio_service.py
from minio import Minio
from datetime import timedelta
from config.settings import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE

# Conexão com o MinIO
cliente_minio = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE
)

def fazer_upload_arquivo(bucket: str, caminho_fisico: str, nome_arquivo_destino: str):
    """Envia o arquivo do HD para o MinIO."""
    # Verifica se o bucket existe, se não, cria
    if not cliente_minio.bucket_exists(bucket):
        cliente_minio.make_bucket(bucket)
        
    cliente_minio.fput_object(bucket, nome_arquivo_destino, caminho_fisico)
    return nome_arquivo_destino

def gerar_url_temporaria(bucket: str, nome_arquivo: str):
    """Gera um link de download direto do MinIO que expira em 5 minutos."""
    url = cliente_minio.presigned_get_object(
        bucket, 
        nome_arquivo, 
        expires=timedelta(minutes=5)
    )
    return url