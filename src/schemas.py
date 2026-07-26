import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class NotaCreate(BaseModel):
    titulo: str = Field(min_length=1)
    contenido: str = ""


class NotaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    titulo: str
    contenido: str
    creado_en: datetime


class NotaDeletedOut(BaseModel):
    id: uuid.UUID
