import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.models import Nota


class NotaRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, titulo: str, contenido: str) -> Nota:
        nota = Nota(titulo=titulo, contenido=contenido)
        self.db.add(nota)
        self.db.commit()
        self.db.refresh(nota)
        return nota

    def obtener(self, nota_id: uuid.UUID) -> Nota | None:
        return self.db.get(Nota, nota_id)

    def buscar(self, query: str | None) -> list[Nota]:
        """Sin query: todas las notas (cubre "listar", FR3). Con query:
        ILIKE sobre titulo o contenido, sin distinguir mayusculas (NFR2)."""
        consulta = self.db.query(Nota)
        if query:
            patron = f"%{query}%"
            consulta = consulta.filter(
                or_(Nota.titulo.ilike(patron), Nota.contenido.ilike(patron))
            )
        return consulta.order_by(Nota.creado_en.desc()).all()

    def eliminar(self, nota: Nota) -> None:
        """DELETE fisico (FR4) - nunca soft delete, a diferencia de
        01_CRUD/02_API/03_SaaS."""
        self.db.delete(nota)
        self.db.commit()
