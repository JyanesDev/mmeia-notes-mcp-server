# Plan de milestones — Notes MCP Server

- [x] M0 — Scaffold del repositorio (estructura, spec/requirements/tasks
      ya versionados desde el commit inicial, no añadidos después)
- [x] M1 — Base de datos (01_Disenar_Base_Datos): Nota (única entidad,
      sin relaciones) — DONE 2026-07-26
      - [x] Verificación de NOT NULL en título/contenido
      - [x] Verificación de `DEFAULT now()` en `creado_en`
      - [x] Verificación de DELETE físico (a diferencia del soft delete
        de las 3 unidades anteriores del catálogo)
      - `disenio.md` (Pasos 1-4) y `db/schema.sql` (Paso 5) creados;
        esquema aplicado y verificado contra un contenedor PostgreSQL 16
        real y desechable (`db/VERIFICATION.md`, Paso 6): 2 pruebas de
        restricción, más verificación del `DEFAULT now()` y del DELETE
        físico. Ningún ADR de proyecto: las 2 restricciones fijadas por
        la spec (sin auth, DELETE físico) ya estaban decididas antes de
        M1; la única decisión de diseño (`Nota.contenido NOT NULL`) no
        tiene alternativa genuinamente abierta, mismo criterio que
        `Organizacion.nombre`/`Proyecto.eliminado_en` en `03_SaaS`.
        Playbook Checklist final: 7/7.
- [x] M2 — API (02_Crear_API): crear/obtener/buscar/eliminar nota, sin
      autenticación (NFR1) — DONE 2026-07-26
      - [x] Tests explícitos: 404 (nota inexistente), búsqueda sin
        resultados, búsqueda case-insensitive
      - `api/contrato.md` (Pasos 1-2, 4 endpoints), estructura en capas
        sin `deps.py`/`security.py` (Paso 3, NFR1), endpoints
        implementados (Paso 4), verificación completa (Paso 6,
        `api/VERIFICATION.md`): 18 tests de pytest + smoke test de 13
        escenarios contra un servidor real, incluida la confirmación
        explícita de que el DELETE es físico de verdad. Cero ADR de
        proyecto (verificado regla-vs-decisión). Playbook Checklist
        final: 5/5.
- [x] M3 — Despliegue (03_Preparar_Despliegue): Docker, CI, verificación
      de 5 puntos, mismo patrón que 01_CRUD/02_API/03_SaaS — despliega
      la API, no el servidor MCP (corre localmente vía stdio) —
      DONE 2026-07-26
      - [x] `docker-compose.yml` con `name: mmeia-notes-mcp-server`
        explícito desde el primer commit (Playbook v0.6.1, aplicando la
        regla añadida tras el incidente real de `03_SaaS`) — sin
        colisión: red creada como `mmeia-notes-mcp-server_default`
      - [x] Verificación de los 5 puntos del Paso 6, incluida una
        espera real de 5 minutos
      - [x] Imagen anterior (`:0.2.0`) reconstruida vía `git worktree`
        + Dockerfile actual, para que la comprobación de "versión
        anterior presente" tenga sustancia real
      - `despliegue.md` (Paso 1), `docker/Dockerfile` (Paso 2, imagen
        `:0.3.0`), `.github/workflows/ci.yml` (Paso 3, validado
        localmente), `docker/docker-compose.yml` + `.env.example`
        (Paso 4), despliegue real (Paso 5), `docs/deployment.md`
        (Paso 6). 18/18 tests de pytest reejecutados tras el bump de
        `APP_VERSION`. Playbook Checklist final: 10/10.
- [ ] M4 — Servidor MCP (04_Crear_MCP): expone crear_nota/obtener_nota/
      buscar_notas/eliminar_nota como Tools
      - [ ] Verificación con MCP Inspector (Paso 5): invocación válida,
        parámetro inválido, recurso inexistente — las 4 Tools
      - [ ] Verificación con un cliente MCP real (Paso 6): las 4 Tools
        listadas por su nombre exacto
      - [ ] Confirmación explícita de que cada Tool mantiene
        correspondencia 1:1 con su endpoint y ninguna contiene lógica de
        negocio propia (FR8/FR10/NFR3, principio del adaptador)
- [ ] M5 — Revisión formal, commit_referencia, congelación v1.0.0
