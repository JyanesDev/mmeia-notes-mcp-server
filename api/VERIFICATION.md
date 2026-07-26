# API verification (Playbook Paso 6, tabla adaptada)

Ejecutado de verdad, no simulado: 18 tests de `pytest` contra un contenedor PostgreSQL 16 real y desechable (`docker run --rm`, destruido después), más un smoke test adicional de arranque real del servidor (`uvicorn`) con peticiones `curl` reales contra 13 escenarios.

A diferencia de `02_API`/`03_SaaS`, esta unidad no aplica JWT (NFR1, decisión deliberada) — la tabla de verificación se reduce a los 4 endpoints reales de `api/contrato.md`, sin la tríada 401/403/404: solo 404 (recurso inexistente) y 422 (validación de Pydantic).

## Tabla de verificación (4 endpoints reales)

| Endpoint | Válido | Body inválido | Inexistente |
|---|---|---|---|
| `POST /api/v1/notas` | 201 ✅ (`contenido` opcional, cadena vacía) | 422 (`titulo` vacío) ✅ | — |
| `GET /api/v1/notas/{id}` | 200 ✅ | — | 404 ✅ |
| `GET /api/v1/notas` | 200 ✅ (con `?q=`, sin `q`, sin resultados) | — | — (sin resultados es `200 []`, nunca 404) ✅ |
| `DELETE /api/v1/notas/{id}` | 200 ✅ (DELETE físico verificado) | — | 404 ✅ |

**El test central del diferenciador de esta unidad:** `test_delete_nota_is_physical_not_soft` — confirma que la fila deja de existir por completo en la base de datos tras el `DELETE` (`db_session.query(Nota)...first() is None`), a diferencia del patrón de soft delete (`eliminado_en`) que `01_CRUD`/`02_API`/`03_SaaS` comparten los tres. `test_search_notas_case_insensitive` verifica NFR2 (`ILIKE`); `test_search_notas_by_titulo`/`test_search_notas_by_contenido` confirman que la búsqueda cubre ambos campos.

## Resultado real de la ejecución (pytest)

```
18 passed, 1 warning in 0.58s
```

El único warning es una `StarletteDeprecationWarning` de la librería (`httpx` con `starlette.testclient`), no relacionado con la lógica del proyecto — mismo tipo de advertencia benigna ya presente en el resto del catálogo.

## Smoke test de arranque real (servidor vivo, no TestClient) — 13 escenarios

```
$ uvicorn src.main:app --port 8002
POST /api/v1/notas (nota 1, "Receta de pan")       → 201 {"id",...,"creado_en"}
POST /api/v1/notas (nota 2, "Lista de la compra")  → 201 {"id",...}
GET  /api/v1/notas/{id-nota-1}                      → 200 (misma nota)
GET  /api/v1/notas/{id-inexistente}                 → 404 {"detail":"nota no encontrada"}
GET  /api/v1/notas?q=pan (coincide titulo Y contenido) → 200 [2 notas]
GET  /api/v1/notas (sin q, listar todas)            → 200 [2 notas]
DELETE /api/v1/notas/{id-nota-1}                    → 200 {"id"} (sin campo eliminado_en)
GET  /api/v1/notas/{id-nota-1} (ya borrada)          → 404
GET  /api/v1/notas (tras borrar)                     → 200 [1 nota]
GET  /api/v1/notas?q=zzz-no-existe                   → 200 [] (nunca 404)
POST /api/v1/notas (sin contenido)                   → 201 {"contenido":""}
POST /api/v1/notas (titulo vacio)                    → 422
GET  /openapi.json, GET /docs (sin token)             → 200, 200
```

Las 13 peticiones produjeron exactamente el código y comportamiento esperado — en particular, la ausencia total de la nota tras el `DELETE` (paso 8, `404` en vez de un `200` con marca de eliminación) es la demostración funcional del diferenciador de esta unidad.

Playbook Checklist final: 5/5 (adaptado a los 4 endpoints reales en vez de los 5 del ejemplo literal).

**Date:** 2026-07-26. **Stack:** FastAPI 0.139.2, SQLAlchemy 2.0.51, PostgreSQL 16. Sin PyJWT ni bcrypt — esta unidad no aplica autenticación (NFR1).
