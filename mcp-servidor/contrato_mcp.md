# Contrato de Tools — Notes MCP Server

Producido siguiendo `04_Playbooks/04_Crear_MCP/PLAYBOOK.md` (Paso 2), a partir de la tabla de endpoints ya verificada de `api/contrato.md` (`02_Crear_API`). Correspondencia 1:1 exigida por FR8/FR10 — ninguna Tool combina, orquesta ni omite operaciones de la API.

## crear_nota
Parámetros: titulo (string), contenido (string)
Devuelve: objeto nota creada (id, titulo, contenido, creado_en)
Invoca: `POST /api/v1/notas`

## obtener_nota
Parámetros: id (string)
Devuelve: objeto nota, o error "no encontrada"
Invoca: `GET /api/v1/notas/{id}`

## buscar_notas
Parámetros: q (string, opcional)
Devuelve: lista de notas (todas si `q` se omite; filtradas por `ILIKE` sobre título/contenido si se indica) — lista vacía si no hay coincidencias, nunca error
Invoca: `GET /api/v1/notas?q=`

## eliminar_nota
Parámetros: id (string)
Devuelve: confirmación del id eliminado, o error "no encontrada"
Invoca: `DELETE /api/v1/notas/{id}`

## Fuera de alcance

Sin Tool `actualizar_nota`: la API no expone `PUT`/`PATCH` (`requirements.md` OUT — sin edición de notas). El servidor MCP no puede exponer una operación que la API no tiene (FR8, FR10).
