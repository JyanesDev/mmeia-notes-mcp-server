-- Generated per 04_Playbooks/01_Disenar_Base_Datos/PLAYBOOK.md (Paso 5), from disenio.md.
-- Single table, no dependencies -- the simplest schema in the catalog so far.

CREATE TABLE Nota (
    id UUID PRIMARY KEY,
    titulo TEXT NOT NULL,
    contenido TEXT NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT now()
);
