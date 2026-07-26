# Diseño de datos

Producido siguiendo `04_Playbooks/01_Disenar_Base_Datos/PLAYBOOK.md` (Pasos 1-4) de MMEIA. Entidad y reglas ya fijadas en `spec.md`/`requirements.md`. Alcance deliberadamente mínimo (`requirements.md` OUT: sin etiquetas, sin categorías, sin usuarios, sin historial, sin adjuntos) — la única entidad de este Reference Project, sin relaciones.

## Nota
- id — identificador único
- titulo — regla: Feature 1 "puede crear una nota con título y contenido"; FR1
- contenido — regla: Feature 1 "puede crear una nota con título y contenido"; FR1
- creado_en — regla: FR1 "nota con `id` y `creado_en`"

No se incluye ningún campo de eliminación (`eliminado_en`): FR4 fija explícitamente DELETE físico, no soft delete — a diferencia de `01_CRUD`/`02_API`/`03_SaaS`, ninguna regla de negocio exige conservar notas eliminadas (ver `disenio.md`/`docs/decisions.md` para la justificación completa, verificada como decisión de diseño y no como regla, antes de documentarla).

No se incluye ninguna columna de búsqueda derivada (`tsvector`, embeddings): NFR2 fija explícitamente comparación simple (`ILIKE`) para la búsqueda de FR3, no full-text ni búsqueda vectorial.

---

## Tipos de dato y clave primaria (Paso 2)

- **Nota:** id (UUID, PK), titulo (TEXT), contenido (TEXT), creado_en (TIMESTAMP)

**Decisión de diseño — UUID como tipo de PK:** verificado con `grep` que `spec.md`/`requirements.md`/`tasks.md` no mencionan `UUID` en ningún punto. Es el propio Paso 2 del Playbook el que lo ofrece como convención por defecto, la misma ya aplicada en `01_CRUD`/`02_API`/`03_SaaS`. Se adopta por consistencia con el resto del catálogo, no por una regla de negocio.

Ningún importe monetario en este dominio — no aplica la comprobación de coma flotante del Paso 2.

## Relaciones y claves foráneas (Paso 3)

Ninguna. `Nota` es la única entidad de este Reference Project — el modelo más simple del catálogo hasta ahora, deliberadamente (`requirements.md` OUT: sin usuarios, sin etiquetas, sin categorías). Sin tabla intermedia N:M, sin FK.

## Restricciones desde las reglas de negocio (Paso 4)

- `Nota.titulo` → `NOT NULL` (Feature 1/FR1: toda nota tiene título)
- `Nota.contenido` → `NOT NULL` — **decisión de diseño, no regla de la spec:** Feature 1 solo exige que el atributo *exista* ("nota con título y contenido"), no que sea obligatorio en cada fila. Mismo criterio ya aplicado a `Tarea.descripcion` en `02_API`/`03_SaaS`: se exige `NOT NULL` para simplificar el modelo (la aplicación nunca necesita distinguir "sin contenido" de "contenido vacío"); puede ser cadena vacía, nunca `NULL`.
- `Nota.creado_en` → `NOT NULL, DEFAULT now()` — a diferencia de `Organizacion.plan`/`Tarea.estado` en unidades anteriores, aquí no hay ninguna ambigüedad que dejar abierta a la capa de aplicación: ninguna regla de negocio condiciona el valor de `creado_en` a una decisión de M2, es simplemente la marca de tiempo de creación — mismo patrón que el propio ejemplo del Playbook (`fecha_registro TIMESTAMP NOT NULL DEFAULT now()`).

Ninguna restricción aquí carece de una regla de negocio o una decisión de diseño explícita que la justifique (criterio de finalización del Paso 4 del Playbook).

**Verificación regla-vs-decisión aplicada antes de este borrador (regla P2 de la retrospectiva del catálogo 2/5):** de las 4 líneas de `disenio.md`, solo `Nota.contenido NOT NULL` es una decisión de diseño sin alternativa genuinamente abierta suficiente para constituir ADR de proyecto — queda registrada aquí, no en `docs/decisions.md`. La ausencia de `eliminado_en` (DELETE físico) y la ausencia de auth ya estaban fijadas explícitamente por `requirements.md` antes de este borrador (FR4, NFR1) — restricciones recibidas, no decisiones tomadas en M1.
