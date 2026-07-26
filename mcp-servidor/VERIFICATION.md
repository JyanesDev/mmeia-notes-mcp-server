# Verificación del servidor MCP

Producida siguiendo `04_Playbooks/04_Crear_MCP/PLAYBOOK.md` (Pasos 5-6). No se dio el servidor por válido sin invocar cada Tool con datos válidos, inválidos y de recurso inexistente, contra infraestructura real (API + PostgreSQL reales, no simulados).

## Paso 5 — MCP Inspector (CLI, `--cli --method tools/call`)

API real en marcha (`uvicorn`, PostgreSQL 16 real y desechable, mismo tipo de infraestructura que `api/VERIFICATION.md`). Servidor MCP arrancado por el propio Inspector vía stdio (`venv/Scripts/python.exe servidor.py`).

`tools/list` confirma los 4 Tools listados exactamente por su nombre — ni más, ni menos:

```
crear_nota, obtener_nota, buscar_notas, eliminar_nota
```

Invocaciones (`tools/call`), respuesta cruda comparada contra `contrato_mcp.md`:

| Tool | Caso | Resultado | Coincide |
|---|---|---|---|
| `crear_nota` | válido (`titulo`, `contenido`) | `201`→objeto nota completo (`id`/`titulo`/`contenido`/`creado_en`) | ✔ |
| `crear_nota` | parámetro inválido (`titulo` omitido) | `isError: true`, error de validación Pydantic (`Field required`) — rechazado antes de llegar a la API | ✔ |
| `obtener_nota` | id existente | objeto nota completo | ✔ |
| `obtener_nota` | id inexistente | `isError: true`, `404: {"detail":"nota no encontrada"}` | ✔ |
| `buscar_notas` | sin `q` | lista con todas las notas existentes | ✔ |
| `buscar_notas` | `q="INSPECTOR"` (mayúsculas) | misma nota, confirma `ILIKE` case-insensitive (NFR2) | ✔ |
| `eliminar_nota` | id existente | `200`→`{"id"}` | ✔ |
| `eliminar_nota` | id ya eliminado | `isError: true`, `404: {"detail":"nota no encontrada"}` | ✔ |
| `obtener_nota` | id recién eliminado | `isError: true`, `404: {"detail":"nota no encontrada"}` — confirma DELETE físico también a través del Tool | ✔ |

**Nota sobre el caso de parámetro inválido:** el ejemplo del Playbook usa un campo vacío (`email=""`); la CLI de MCP Inspector no acepta un valor vacío tras `=` (`Invalid parameter format`, limitación propia de esa herramienta, no del servidor). Se usó en su lugar la omisión del parámetro requerido `titulo` — mismo tipo de fallo (validación de entrada antes de llegar a la lógica de negocio), verificado como `isError: true` con el mensaje real de Pydantic, cumpliendo el mismo criterio de la tabla de verificación ("Parámetro inválido").

Las 8 invocaciones producen exactamente lo esperado — ninguna requirió reinterpretar la respuesta de la API: los Tools son adaptadores puros (NFR3), el error `404` de la API llega intacto hasta el cliente.

## Paso 6 — Cliente MCP real

Cliente usado: **Claude Code**, cliente MCP real oficial (mismo estatus que Claude Desktop en la lista de clientes de modelcontextprotocol.io) — usado en vez de Claude Desktop porque es el cliente disponible en este entorno.

Registro del servidor con ruta absoluta (`claude mcp add notes-mcp -e NOTES_API_BASE=http://localhost:8000 -- <ruta absoluta al intérprete del venv> <ruta absoluta a servidor.py>`), confirmado con `claude mcp get notes-mcp`:

```
notes-mcp:
  Status: ✔ Connected
  Type: stdio
```

**Reinicio completo del cliente:** se lanzó un proceso `claude` completamente nuevo y separado de la sesión actual (no una recarga de la misma sesión — el mismo criterio que exige el Paso 6, "no basta con recargar la ventana"), con el único propósito de listar los Tools disponibles del servidor `notes-mcp`. Resultado exacto:

```
mcp__notes-mcp__buscar_notas
mcp__notes-mcp__crear_nota
mcp__notes-mcp__eliminar_nota
mcp__notes-mcp__obtener_nota
```

**Los 4 nombres exactos de `contrato_mcp.md` aparecen — ni más, ni menos, ni con nombres distintos** (el prefijo `mcp__notes-mcp__` es la convención de espacio de nombres de este cliente para servidores MCP registrados, no una alteración del nombre del Tool). Confirmado como un hecho observable — ningún Tool fue invocado a través de este cliente para esta verificación, siguiendo la prohibición explícita del Playbook de usar la conversación con un modelo como mecanismo de validación; la validación funcional completa ya se ejecutó en el Paso 5.
