# Requisitos — Notes MCP Server

## Funcionales
FR1.  Crear nota (`titulo`, `contenido`) -> nota con `id` y `creado_en`.
FR2.  Obtener una nota existente por `id`.
FR3.  Buscar notas por palabra clave en `titulo` o `contenido`, sin
      distinguir mayúsculas/minúsculas; sin palabra clave, devuelve
      todas.
FR4.  Eliminar una nota de forma permanente (DELETE físico, nunca soft
      delete — ninguna regla exige conservar notas eliminadas).
FR5.  404 si la nota no existe (crear/obtener/eliminar).
FR6.  Contrato versionado en /api/v1.
FR7.  OpenAPI generado automáticamente desde el framework, accesible
      sin autenticación.
FR8.  Toda Tool del servidor MCP invoca exclusivamente un endpoint de
      la API — ninguna Tool implementa lógica de negocio propia
      (Feature 5, principio del adaptador).
FR9.  El servidor MCP expone exactamente 4 Tools: crear_nota,
      obtener_nota, buscar_notas, eliminar_nota — verificadas primero
      con un cliente de inspección (MCP Inspector) y después con un
      cliente MCP real (Claude Desktop u equivalente).
FR10. Cada Tool debe mantener una correspondencia 1:1 con una operación
      pública de la API — ninguna Tool combina, orquesta ni omite
      operaciones; consecuencia directa de Feature 5 (principio del
      adaptador).

## No funcionales
NFR1. Ningún endpoint de la API requiere autenticación — decisión
      deliberada, no omisión: la autenticación ya está demostrada en
      02_API/03_SaaS; repetirla aquí no aportaría nada a la tesis de
      esta unidad (integración MCP).
NFR2. La búsqueda (FR3) usa comparación simple (ILIKE), nunca full-text
      search ni búsqueda vectorial — proporcionada a la simplicidad del
      dominio; full-text/embeddings pertenecen a 05_RAG.
NFR3. Las Tools actuarán únicamente como adaptadores del protocolo MCP
      hacia la API. Cualquier lógica de negocio deberá residir
      exclusivamente en la API — criterio arquitectónico, no un detalle
      físico como el número de líneas (más robusto frente a refactors
      de formato o estilo que no cambien la responsabilidad real de
      cada capa).

## Alcance explícito (IN / OUT)
IN:  CRUD mínimo de una única entidad (Nota), búsqueda simple por
     palabra clave, servidor MCP que expone 4 operaciones como Tools,
     verificación con MCP Inspector y con un cliente MCP real,
     despliegue de la API (Docker/CI, igual que las 3 unidades
     anteriores del catálogo).
OUT: autenticación, multi-tenencia, etiquetas/categorías, edición de
     notas (sin Tool de actualizar), historial de versiones, adjuntos,
     full-text search, búsqueda vectorial/embeddings, Resources y
     Prompts de MCP (solo Tools — posible evolución futura del
     Playbook, no de este proyecto), despliegue del propio servidor MCP
     como servicio remoto (corre localmente vía stdio, mismo modelo que
     el propio Playbook 04_Crear_MCP).
