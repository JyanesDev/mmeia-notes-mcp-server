import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.repositories import NotaRepository


class NotaService:
    def __init__(self, db: Session):
        self.notas = NotaRepository(db)

    def crear(self, titulo: str, contenido: str):
        return self.notas.crear(titulo=titulo, contenido=contenido)

    def obtener_autorizada(self, nota_id: uuid.UUID):
        """Sin autenticacion (NFR1): "autorizada" aqui solo significa
        "existe" - no hay ownership ni tenencia que verificar."""
        nota = self.notas.obtener(nota_id)
        if nota is None:
            raise HTTPException(status_code=404, detail="nota no encontrada")
        return nota

    def buscar(self, query: str | None):
        return self.notas.buscar(query)

    def eliminar(self, nota_id: uuid.UUID):
        nota = self.obtener_autorizada(nota_id)
        self.notas.eliminar(nota)  # DELETE fisico (FR4)
        return nota_id
