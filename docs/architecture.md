# Architecture

```text
Client --HTTP--> API (FastAPI) --SQL--> PostgreSQL
```

Un único servicio API y una única base de datos relacional — sin autenticación (NFR1), sin cola de mensajes, sin caché. `requirements.md` OUT excluye explícitamente auth, multi-tenencia y full-text/embeddings, así que nada de eso está justificado aquí.

## Capas dentro de la API

```text
routers/      -> HTTP concerns only (parsing, status codes) — notas.py
services.py   -> reglas: "existe" (obtener_autorizada), DELETE físico
repositories.py -> persistencia (SQLAlchemy), búsqueda ILIKE
models.py     -> modelo SQLAlchemy, mapeado 1:1 a db/schema.sql (M1)
schemas.py    -> modelos Pydantic de request/response
```

Sin `deps.py` ni `security.py`: a diferencia de `02_API`/`03_SaaS`, esta unidad no tiene capa de autenticación — decisión deliberada (NFR1), no una carencia. `NotaService.obtener_autorizada` conserva el nombre por consistencia con el resto del catálogo, pero aquí "autorizada" significa únicamente "existe" — no hay ownership ni tenencia que verificar.

## Esta API como pieza de un sistema mayor (M4)

Esta API es, en sí misma, un Reference Project de `02_Crear_API` — pero su propósito final en este proyecto es ser **la única fuente de lógica de negocio** que el servidor MCP (M4) invocará como adaptador puro (Feature 5, `spec.md`). Cada endpoint aquí definido tiene, por diseño, una correspondencia 1:1 con una futura Tool: `crear_nota`→`POST /api/v1/notas`, `obtener_nota`→`GET /api/v1/notas/{id}`, `buscar_notas`→`GET /api/v1/notas`, `eliminar_nota`→`DELETE /api/v1/notas/{id}`.

## Qué esto deliberadamente no incluye

- Sin autenticación ni autorización real — ya demostradas en `02_API`/`03_SaaS` (NFR1).
- Sin edición de notas (`PUT`/`PATCH`) — ninguna FR lo exige (`requirements.md` OUT).
- Sin full-text search ni búsqueda vectorial — `ILIKE` simple basta para el alcance (NFR2); esos conceptos pertenecen a `05_RAG`.
