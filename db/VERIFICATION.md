# Schema verification (Playbook Paso 6)

Executed against a real, disposable `postgres:16` container (`docker run --rm -d --name mmeia-mcp-verify`), not simulated. Container stopped after verification; `--rm` removed it immediately.

## 1. Apply schema.sql

```
CREATE TABLE
```

1 table created without errors — the simplest schema in the catalog so far (single entity, no relations).

## 2. Base data (valid) — `DEFAULT now()` verification

Inserted a `Nota` without specifying `creado_en`: `INSERT 0 1`. Queried back: `creado_en` populated automatically (`2026-07-26 18:20:54.701924`) — confirms the `DEFAULT now()` constraint works as designed, no application-layer value required.

## 3. Constraint tests (each expected to fail)

| # | Test | Real result |
|---|---|---|
| 1 | `Nota.titulo` nulo | `ERROR: null value in column "titulo" of relation "nota" violates not-null constraint` |
| 2 | `Nota.contenido` nulo | `ERROR: null value in column "contenido" of relation "nota" violates not-null constraint` |

Both failed exactly as `disenio.md` required — none passed silently, none failed for the wrong reason.

## 4. DELETE físico verification (`tasks.md` M1, comprobación explícita — a diferencia de las 3 unidades anteriores)

Verifica que FR4 (DELETE físico, nunca soft delete) se cumple realmente en el esquema — a diferencia de `01_CRUD`/`02_API`/`03_SaaS`, que preservan la fila con un campo `eliminado_en`.

| Paso | Acción | Resultado real |
|---|---|---|
| 1 | Contar notas | `count = 1` |
| 2 | `DELETE FROM Nota WHERE id = ...` (físico, nunca `UPDATE`) | `DELETE 1` |
| 3 | Contar filas con ese `id` de nuevo | `count = 0` — la fila ya **no existe**, a diferencia del patrón de soft delete de las 3 unidades anteriores |

Comportamiento exactamente como exige FR4 ("DELETE físico, nunca soft delete").

## 5. Estado final

```
        List of relations
 Schema | Name | Type  |  Owner
--------+------+-------+----------
 public | nota | table | postgres
(1 row)
```

Playbook Checklist final, casilla 7 ("Las pruebas de restricción fallan exactamente como se describe"): satisfecho. Las verificaciones explícitas de `tasks.md` M1 (NOT NULL en título/contenido) cubiertas con evidencia real, más la verificación adicional del `DEFAULT now()` y del DELETE físico, ambas centrales al diferenciador de esta unidad frente al resto del catálogo.

**Date:** 2026-07-26. **Engine:** PostgreSQL 16 (official Docker image, `postgres:16`).
