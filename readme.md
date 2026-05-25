# 📄 Sistema Gerenciador de Documentos

Este repositório armazena o código-fonte do sistema de gerenciamento de documentos, desenvolvido por **Cauan, Gian, Gustavo e Hallyson**.

---

## ⚙️ Pré-requisitos

- **Node.js** (v20.19.0 ou superior)  
- **Python** (v3.8 ou superior)
- **PostgreSQL** (Instalado e ativo na máquina local)

---
## Rodar via Script
1. tornar o arquivo run.sh executável: chmod +x run.sh
2. rodar o arquivo: ./run.sh

---

## 🚀 Como rodar o Back-end e configurar Banco de dados (FastAPI e Postgres)

1. Acesse a pasta do servidor:
cd back-end

2. Crie e ative o ambiente virtual:
python3 -m venv venv
source venv/bin/activate

3. Instale as dependências:
pip install -r requirements.txt

4. Criar arquivo **`.env`** dentro da pasta `back-end/`:
   - GEMINI_API_KEY=**`SuaChaveAqui`**
   - Substitua **`'usuario'`** e **`'senha'`** (deixe por padrão o usuario como **`"postgres"`**)
     - DATABASE_URL=postgresql://usuario:senha@localhost:5432/gerenciador_documentos
5. Criar Banco de dados: python init_db.py

6. Inicie a API:
uvicorn main:app --reload

A API estará disponível em:
http://127.0.0.1:8000/

---

## 💻 Como rodar o Front-end (Vue 3 + Vite)

1. Abra um novo terminal e acesse a pasta da interface:
cd front-end

2. Instale as dependências do projeto:
npm install

3. Inicie o servidor de desenvolvimento:
npm run dev

O front-end estará disponível em:
http://localhost:5173/

---

## Para realizar testes, usar o chrome com o CORS desativado!
**rode isso no terminal:**
- google-chrome --disable-web-security --user-data-dir="/tmp/chrome_dev_cors"
