import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String, Text, BigInteger, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome_original = Column(String(255), nullable=False)
    resumo_ia = Column(Text, nullable=True)
    mimetype = Column(String(100), nullable=False)
    tamanho = Column(BigInteger, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(UUID(as_uuid=True), nullable=True)
    vetor_resumo = Column(Vector(768), nullable=True)