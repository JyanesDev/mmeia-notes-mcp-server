from src.models import Nota

from tests.conftest import _crear_nota


# --- POST /api/v1/notas ---

def test_create_nota_success(client):
    resp = _crear_nota(client, titulo="Idea de proyecto", contenido="Notas MCP server")
    assert resp.status_code == 201
    body = resp.json()
    assert body["titulo"] == "Idea de proyecto"
    assert body["contenido"] == "Notas MCP server"
    assert "id" in body
    assert "creado_en" in body  # FR1: DEFAULT now() poblado, verificado en M1


def test_create_nota_empty_titulo_is_422(client):
    resp = client.post("/api/v1/notas", json={"titulo": "", "contenido": "x"})
    assert resp.status_code == 422


def test_create_nota_default_contenido_is_empty_string(client):
    """FR1: contenido acepta cadena vacia, nunca requerido no-vacio."""
    resp = client.post("/api/v1/notas", json={"titulo": "Solo titulo"})
    assert resp.status_code == 201
    assert resp.json()["contenido"] == ""


def test_create_nota_no_auth_required(client):
    """NFR1: ningun endpoint requiere autenticacion - no hay cabecera que enviar."""
    resp = _crear_nota(client)
    assert resp.status_code == 201


# --- GET /api/v1/notas/{id} ---

def test_get_nota_success(client):
    nota = _crear_nota(client, titulo="Mi nota").json()
    resp = client.get(f"/api/v1/notas/{nota['id']}")
    assert resp.status_code == 200
    assert resp.json()["titulo"] == "Mi nota"


def test_get_nota_not_found_is_404(client):
    resp = client.get("/api/v1/notas/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


# --- GET /api/v1/notas (buscar_notas) ---

def test_list_all_notas_without_query(client):
    _crear_nota(client, titulo="Primera")
    _crear_nota(client, titulo="Segunda")
    resp = client.get("/api/v1/notas")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_search_notas_by_titulo(client):
    _crear_nota(client, titulo="Receta de pan", contenido="harina, agua, sal")
    _crear_nota(client, titulo="Lista de la compra", contenido="leche, huevos")
    resp = client.get("/api/v1/notas?q=pan")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 1
    assert body[0]["titulo"] == "Receta de pan"


def test_search_notas_by_contenido(client):
    _crear_nota(client, titulo="Receta de pan", contenido="harina, agua, sal")
    _crear_nota(client, titulo="Lista de la compra", contenido="leche, huevos")
    resp = client.get("/api/v1/notas?q=huevos")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 1
    assert body[0]["titulo"] == "Lista de la compra"


def test_search_notas_case_insensitive(client):
    """NFR2: ILIKE, sin distinguir mayusculas/minusculas."""
    _crear_nota(client, titulo="Receta de PAN")
    resp = client.get("/api/v1/notas?q=pan")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_search_notas_no_results_is_200_empty_not_404(client):
    _crear_nota(client, titulo="Algo")
    resp = client.get("/api/v1/notas?q=inexistente")
    assert resp.status_code == 200
    assert resp.json() == []


# --- DELETE /api/v1/notas/{id} (DELETE fisico) ---

def test_delete_nota_success(client):
    nota = _crear_nota(client).json()
    resp = client.delete(f"/api/v1/notas/{nota['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == nota["id"]


def test_delete_nota_not_found_is_404(client):
    resp = client.delete("/api/v1/notas/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


def test_delete_nota_is_physical_not_soft(client, db_session):
    """FR4: DELETE fisico, a diferencia de 01_CRUD/02_API/03_SaaS - la fila
    deja de existir por completo, no queda marcada con un campo eliminado_en."""
    nota = _crear_nota(client, titulo="A borrar").json()

    resp = client.delete(f"/api/v1/notas/{nota['id']}")
    assert resp.status_code == 200
    assert "eliminado_en" not in resp.json()  # a diferencia del resto del catalogo

    fila = db_session.query(Nota).filter(Nota.id == nota["id"]).first()
    assert fila is None  # la fila ya NO existe - nunca un soft delete


def test_get_deleted_nota_returns_404(client):
    nota = _crear_nota(client, titulo="A borrar").json()
    client.delete(f"/api/v1/notas/{nota['id']}")

    resp = client.get(f"/api/v1/notas/{nota['id']}")
    assert resp.status_code == 404


def test_deleted_nota_excluded_from_search(client):
    nota = _crear_nota(client, titulo="Nota temporal").json()
    client.delete(f"/api/v1/notas/{nota['id']}")

    resp = client.get("/api/v1/notas")
    assert resp.status_code == 200
    assert resp.json() == []


# --- Feature 6 / FR7: OpenAPI accesible sin autenticacion ---

def test_openapi_json_accessible_without_auth(client):
    resp = client.get("/openapi.json")
    assert resp.status_code == 200


def test_docs_accessible_without_auth(client):
    resp = client.get("/docs")
    assert resp.status_code == 200
