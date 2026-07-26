import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas import NotaCreate, NotaOut, NotaDeletedOut
from src.services import NotaService

router = APIRouter(prefix="/api/v1/notas", tags=["notas"])


@router.post("", response_model=NotaOut, status_code=201)
def crear_nota(payload: NotaCreate, db: Session = Depends(get_db)):
    return NotaService(db).crear(titulo=payload.titulo, contenido=payload.contenido)


@router.get("", response_model=list[NotaOut])
def buscar_notas(q: str | None = None, db: Session = Depends(get_db)):
    return NotaService(db).buscar(q)


@router.get("/{nota_id}", response_model=NotaOut)
def obtener_nota(nota_id: uuid.UUID, db: Session = Depends(get_db)):
    return NotaService(db).obtener_autorizada(nota_id)


@router.delete("/{nota_id}", response_model=NotaDeletedOut)
def eliminar_nota(nota_id: uuid.UUID, db: Session = Depends(get_db)):
    eliminado_id = NotaService(db).eliminar(nota_id)
    return {"id": eliminado_id}
