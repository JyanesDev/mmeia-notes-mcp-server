# Spec — Notes MCP Server

## Feature 1: Crear nota
Un cliente (vía la API, o indirectamente vía un Tool MCP) puede crear una
nota con título y contenido. La nota queda disponible de inmediato para
consulta y búsqueda.

## Feature 2: Obtener nota por id
Cualquier nota existente puede recuperarse por su identificador único.

## Feature 3: Buscar notas por palabra clave
Las notas pueden buscarse por una palabra clave que coincida con el título
o el contenido, sin distinguir mayúsculas/minúsculas. Sin palabra clave,
la búsqueda devuelve todas las notas — no existe un endpoint de listado
separado.

## Feature 4: Eliminar nota
Una nota puede eliminarse permanentemente. A diferencia de los proyectos
anteriores del catálogo, esta unidad usa DELETE físico, no soft delete:
ninguna regla de negocio exige conservar notas eliminadas.

## Feature 5: Servidor MCP como adaptador, nunca como lógica propia
Un servidor MCP expone las Features 1-4 como Tools (`crear_nota`,
`obtener_nota`, `buscar_notas`, `eliminar_nota`), verificado primero con
un cliente de inspección y después con un cliente MCP real (04_Crear_MCP).

Principio rector de esta unidad, más importante que cualquier otro detalle
de implementación: **toda Tool es una adaptación directa de una operación
ya existente de la API — nunca reimplementa lógica propia.**

```
Tool MCP
    ↓
Servidor MCP
    ↓
Endpoint HTTP
    ↓
Servicio de aplicación
    ↓
Base de datos
```

Nunca:

```
Tool MCP → lógica propia → Base de datos
```

Si una Tool alguna vez necesita más lógica de la que su endpoint ya
ofrece, la lógica se añade a la API (Feature 1-4), nunca al servidor MCP.

## Feature 6: Contrato y documentación viva
La API expone automáticamente una especificación OpenAPI actualizada,
igual que el resto del catálogo.
