# Decisiones (ADR del proyecto)

**M1-M2: cero ADR de proyecto**, verificado explícitamente antes de escribir esta sección (regla P2 de la retrospectiva del catálogo 2/5, ya aplicada en `03_SaaS`). Las tres restricciones que podrían parecer decisiones de ingeniería ya estaban fijadas por `spec.md`/`requirements.md` antes de M1/M2, sin ninguna alternativa realmente abierta en el momento de implementar:

- **DELETE físico, nunca soft delete** — fijado por FR4 desde el diseño conceptual, no una decisión de M1/M2.
- **Sin autenticación** — fijado por NFR1 desde el diseño conceptual, no una decisión de M2.
- **Búsqueda `ILIKE` simple, nunca full-text/embeddings** — fijado por NFR2 desde el diseño conceptual, no una decisión de M2.

La única decisión de diseño real detectada (`Nota.contenido NOT NULL`, en `disenio.md` de M1) tampoco tiene alternativa genuinamente abierta suficiente para constituir un ADR — registrada allí, no aquí.

Este documento permanece deliberadamente vacío de ADR-RP a la espera de M3 (despliegue) y M4 (servidor MCP), donde sí podrían aparecer decisiones reales (p. ej. cómo estructurar el proyecto separado del servidor MCP). Antes de documentar cualquier decisión futura, se repetirá la misma verificación regla-vs-decisión.
