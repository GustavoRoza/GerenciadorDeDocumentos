@echo off
echo ==========================================
echo   INICIANDO O GERENCIADOR DE DOCUMENTOS
echo ==========================================

echo.
echo [1/4] Verificando dependencia do MinIO...
if not exist minio.exe (
    echo MinIO nao encontrado. Baixando a versao para Windows...
    powershell -Command "Invoke-WebRequest -Uri 'https://dl.min.io/server/minio/release/windows-amd64/minio.exe' -OutFile 'minio.exe'"
    echo Download do MinIO concluido.
)

if not exist dados-minio mkdir dados-minio

echo Iniciando o Servidor MinIO...
:: Abre o MinIO em uma nova janela
start "MinIO Server" cmd /k "minio.exe server ./dados-minio --console-address :9001"

echo.
echo [2/4] Configurando o Back-end (Python/FastAPI)...
cd back-end
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)
call .\venv\Scripts\activate.bat

echo Instalando dependencias...
pip install -r requirements.txt

echo Sincronizando Banco de Dados...
python init_db.py

:: Abre o Backend em uma nova janela
start "Back-end (FastAPI)" cmd /k "uvicorn main:app --reload"
cd ..

echo.
echo [3/4] Configurando o Front-end (Vue/Vite)...
cd front-end
if not exist node_modules (
    echo Instalando pacotes Node...
    call npm install
)

:: Abre o Frontend em uma nova janela
start "Front-end (Vue 3)" cmd /k "npm run dev"
cd ..

echo.
echo ==========================================
echo [4/4] TUDO PRONTO! SISTEMAS RODANDO:
echo - MinIO (Console): http://127.0.0.1:9001
echo - Back-end:        http://127.0.0.1:8000
echo - Front-end:       http://localhost:5173
echo ==========================================
pause