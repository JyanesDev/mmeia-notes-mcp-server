# Contrato de la API

Producido siguiendo `04_Playbooks/02_Crear_API/PLAYBOOK.md` (Pasos 1-2). Cada endpoint corresponde a una operación real ya fijada en `spec.md`/`requirements.md` — ninguno especulativo.

**Sin autenticación (NFR1), a diferencia de `02_API`/`03_SaaS`:** decisión deliberada, no omisión — ver `requirements.md`. Esta API es la única responsable de la lógica de negocio; el servidor MCP de M4 la invoca sin añadir ninguna capa propia (Feature 5, principio del adaptador).

## Tabla de endpoints (Paso 1)

| Endpoint | Operación real |
|---|---|
| `POST /api/v1/notas` | crear nota — FR1 |
| `GET /api/v1/notas/{id}` | obtener nota por id — FR2 |
| `GET /api/v1/notas` | buscar por palabra clave (`?q=`), o listar todas sin `q` — FR3 |
| `DELETE /api/v1/notas/{id}` | eliminar de forma permanente (DELETE físico) — FR4 |

No se incluye ningún endpoint de edición (`PUT`/`PATCH`): ninguna FR lo exige (`requirements.md` OUT: "edición de notas"). `GET /docs` y `GET /openapi.json` (Feature 6, FR7) no se listan como endpoint de negocio: los genera automáticamente el framework.

## Contratos (Paso 2)

### `POST /api/v1/notas`
Request: `{"titulo": str, "contenido": str}` → **201** `{"id","titulo","contenido","creado_en"}` | **422** (`titulo` vacío — validación de Pydantic antes de llegar al servicio)

`contenido` acepta cadena vacía (`""`), nunca `null` — `disenio.md` M1 fija `NOT NULL` sin exigir contenido no vacío (misma decisión que `Tarea.descripcion` en `02_API`/`03_SaaS`).

### `GET /api/v1/notas/{id}`
→ **200** `{"id","titulo","contenido","creado_en"}` | **404** (no existe — FR5)

### `GET /api/v1/notas`
Query: `?q=` (opcional) → **200** `[{"id","titulo","contenido","creado_en"}, ...]`

Sin `q`: devuelve todas las notas (cubre "listar", FR3 — no existe un endpoint de listado separado). Con `q`: filtra por `ILIKE` sobre `titulo` **o** `contenido`, sin distinguir mayúsculas/minúsculas (NFR2). Sin resultados: `200 []`, nunca `404` — una búsqueda vacía no es un error.

### `DELETE /api/v1/notas/{id}`
→ **200** `{"id"}` (DELETE físico — FR4, la fila deja de existir; verificado en `db/VERIFICATION.md` de M1) | **404** (no existe — FR5)

No hay cuerpo `eliminado_en` en la respuesta, a diferencia de `01_CRUD`/`02_API`/`03_SaaS`: no hay ningún campo que reflejar, la nota ya no existe.
