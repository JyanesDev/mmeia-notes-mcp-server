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
- [ ] M2 — API (02_Crear_API): crear/obtener/buscar/eliminar nota, sin
      autenticación (NFR1)
      - [ ] Tests explícitos: 404 (nota inexistente), búsqueda sin
        resultados, búsqueda case-insensitive
- [ ] M3 — Despliegue (03_Preparar_Despliegue): Docker, CI, verificación
      de 5 puntos, mismo patrón que 01_CRUD/02_API/03_SaaS — despliega
      la API, no el servidor MCP (corre localmente vía stdio)
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
