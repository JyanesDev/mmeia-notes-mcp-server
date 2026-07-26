import uuid

from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.sql import func

from src.database import Base

# db/schema.sql (M1) is the single authoritative DDL - produced by
# 01_Disenar_Base_Datos and verified in db/VERIFICATION.md. This model
# maps to that table; it deliberately does NOT redeclare constraints
# already enforced by the real schema (same reasoning as 01_CRUD/02_API/03_SaaS).


class Nota(Base):
    __tablename__ = "nota"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(Text, nullable=False)
    contenido = Column(Text, nullable=False)
    creado_en = Column(TIMESTAMP, nullable=False, server_default=func.now())
