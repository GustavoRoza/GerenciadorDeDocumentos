CREATE DATABASE gerenciador_documentos;

\c gerenciador_documentos;

-- buscas vetoriais
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documentos (
    id UUID PRIMARY KEY,
    nome_original VARCHAR(255) NOT NULL,
    resumo_ia TEXT,
    vetor_resumo vector(768), -- Coordenadas
    mimetype VARCHAR(100) NOT NULL,
    tamanho BIGINT NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    usuario_id UUID
);