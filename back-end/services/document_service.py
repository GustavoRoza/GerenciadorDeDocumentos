from sqlalchemy.orm import Session
import models

def buscar_documentos_no_banco(q: str, db: Session):
    """
    Realiza a consulta no banco de dados buscando documentos
    pelo nome original ou pelo resumo gerado pela IA.
    """
    query = db.query(models.Documento)
    
    if q:
        # Filtra onde o resumo OU o nome original contenham o termo pesquisado
        query = query.filter(
            (models.Documento.resumo_ia.ilike(f"%{q}%")) |
            (models.Documento.nome_original.ilike(f"%{q}%"))
        )
        
    documentos = query.order_by(models.Documento.data_criacao.desc()).all()
    
    # Formatando o resultado para evitar erro de conversão de UUID e Datas no JSON
    resultado = []
    for doc in documentos:
        resultado.append({
            "id": str(doc.id),
            "nome_original": doc.nome_original,
            "resumo_ia": doc.resumo_ia,
            "mimetype": doc.mimetype,
            "tamanho": doc.tamanho,
            "data_criacao": doc.data_criacao.isoformat() if doc.data_criacao else None
        })
        
    return resultado