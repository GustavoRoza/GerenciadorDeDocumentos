# config/settings.py

# Configurações do MinIO
MINIO_ENDPOINT = "127.0.0.1:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_SECURE = False # Mude para True se usar HTTPS no futuro
BUCKET_NAME = "teste"

# Configurações do Banco de Dados (Exemplo)
DB_CONFIG = {
    "host": "localhost",
    "database": "meubanco",
    "user": "usuario",
    "password": "123"
}