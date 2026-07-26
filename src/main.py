from fastapi import FastAPI

from src.routers import notas

# Bumped on each deployment milestone (03_Preparar_Despliegue, Paso 6 punto 3).
APP_VERSION = "0.3.0"

app = FastAPI(title="mmeia-notes-mcp-server", version=APP_VERSION)

app.include_router(notas.router)


@app.get("/health")
def health():
    return {"status": "ok", "version": APP_VERSION}
