import os

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes-mcp")
API_BASE = os.environ.get("NOTES_API_BASE", "http://localhost:8000")


def _raise_with_api_detail(r: httpx.Response) -> None:
    """Propaga el error tal como lo devuelve la API, sin reinterpretarlo (NFR3)."""
    if r.is_error:
        raise ValueError(f"{r.status_code}: {r.text}")


@mcp.tool()
def crear_nota(titulo: str, contenido: str) -> dict:
    """Crea una nota en la API de notas."""
    r = httpx.post(f"{API_BASE}/api/v1/notas", json={"titulo": titulo, "contenido": contenido})
    _raise_with_api_detail(r)
    return r.json()


@mcp.tool()
def obtener_nota(id: str) -> dict:
    """Obtiene una nota por id."""
    r = httpx.get(f"{API_BASE}/api/v1/notas/{id}")
    _raise_with_api_detail(r)
    return r.json()


@mcp.tool()
def buscar_notas(q: str = "") -> list:
    """Busca notas por palabra clave en titulo o contenido; sin `q`, devuelve todas."""
    params = {"q": q} if q else {}
    r = httpx.get(f"{API_BASE}/api/v1/notas", params=params)
    _raise_with_api_detail(r)
    return r.json()


@mcp.tool()
def eliminar_nota(id: str) -> dict:
    """Elimina una nota de forma permanente."""
    r = httpx.delete(f"{API_BASE}/api/v1/notas/{id}")
    _raise_with_api_detail(r)
    return r.json()


if __name__ == "__main__":
    mcp.run()
