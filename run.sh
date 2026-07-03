#!/bin/bash

echo "Limpando portas presas..."
fuser -k 8000/tcp 2>/dev/null
fuser -k 5173/tcp 2>/dev/null
fuser -k 9000/tcp 2>/dev/null
fuser -k 9001/tcp 2>/dev/null

echo "Verificando dependência do MinIO..."
if [ ! -f "./minio" ]; then
    echo "MinIO não encontrado. Baixando a versão para Linux..."
    wget -q https://dl.min.io/server/minio/release/linux-amd64/minio -O minio
    chmod +x minio
    echo "Download do MinIO concluído."
fi

echo "Iniciando o MinIO..."
mkdir -p dados-minio
# Executa o binário local baixado
./minio server ./dados-minio --console-address ":9001" &
PID_MINIO=$!

echo "Iniciando o Back-end (FastAPI)..."
cd back-end

if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual (venv)..."
    python3 -m venv venv
fi

source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "Verificando e instalando dependências do requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "AVISO: requirements.txt não encontrado! Instalando dependências padrão..."
    pip install --upgrade pip
    pip install fastapi uvicorn python-multipart google-generativeai python-dotenv sqlalchemy psycopg2-binary minio pgvector
fi

uvicorn main:app --reload &
PID_BACK=$!
cd ..

echo "Aguardando o Back-end ficar online..."
while ! curl -s http://127.0.0.1:8000/ > /dev/null; do
    sleep 1
done
echo "Back-end online!"

echo "Iniciando o Front-end (Vue/Vite)..."
cd front-end
npm install
npm run dev &
PID_FRONT=$!
cd ..

echo "Abrindo o sistema no navegador..."
google-chrome "http://localhost:5173" 2>/dev/null &

trap "echo ' Encerrando servidores...'; kill $PID_BACK $PID_FRONT $PID_MINIO 2>/dev/null; exit" SIGINT EXIT

echo "Sistemas rodando com CORS configurado. Pressione Ctrl+C para parar."
wait
