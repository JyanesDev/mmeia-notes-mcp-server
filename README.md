# 🔌 Notes MCP Server

![Category](https://img.shields.io/badge/MMEIA-04_MCP-6f42c1)
![Status](https://img.shields.io/badge/status-M0--M4%20complete-success)

Notes API plus MCP adapter built as the **fourth MMEIA Reference Project**.

## 📍 Portfolio Position

| Field | Value |
|---|---|
| Collection | MMEIA Reference Projects |
| Reference | `04_MCP` |
| Category | MCP / AI integration |
| Domain | Notes |
| Focus | Expose an existing API through MCP without duplicating application logic |

## 🎯 What This Project Demonstrates

- Notes REST API
- Four MCP operations: create, get, search and delete notes
- 1:1 mapping between MCP operations and API endpoints
- PostgreSQL persistence
- API verification with Pytest
- MCP verification with Inspector
- Docker deployment for the API

## 🛠 Tech Stack

| Area | Technology |
|---|---|
| API | FastAPI + Uvicorn |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2 |
| Validation | Pydantic |
| MCP | Official `mcp` SDK + FastMCP |
| HTTP | HTTPX |
| Tests | Pytest |
| Deployment | Docker + Docker Compose |
| CI | GitHub Actions |

## 🏗 Architecture

```text
MCP consumer
    ↓
MCP adapter
    ↓
Notes API
    ↓
PostgreSQL
```

The MCP layer is intentionally thin. The application rules remain in the API.

## ✅ Current Status

| Milestone | State |
|---|---|
| M0 — Scaffold | ✅ Complete |
| M1 — Database | ✅ Complete |
| M2 — Notes API | ✅ Complete — 18 Pytest tests |
| M3 — Deployment | ✅ Complete |
| M4 — MCP adapter | ✅ Complete — 4 operations verified |
| M5 — Formal freeze | ⏳ Pending |

## 📂 Repository Structure

```text
.
├── spec.md
├── requirements.md
├── tasks.md
├── api/
├── db/
├── docs/
├── src/
├── tests/
├── docker/
├── mcp-servidor/
└── contrato_mcp.md
```

## 📚 Key Documentation

- [`spec.md`](spec.md) — project scope and behaviour
- [`requirements.md`](requirements.md) — requirements
- [`tasks.md`](tasks.md) — milestones and progress
- [`api/contrato.md`](api/contrato.md) — REST API contract
- [`contrato_mcp.md`](contrato_mcp.md) — MCP contract
- [`api/VERIFICATION.md`](api/VERIFICATION.md) — API evidence
- [`mcp-servidor/VERIFICATION.md`](mcp-servidor/VERIFICATION.md) — MCP evidence
- [`docs/deployment.md`](docs/deployment.md) — deployment evidence

## 🧭 MMEIA Reference Projects

| # | Category | Repository |
|---|---|---|
| 01 | 🗃️ CRUD | [mmeia-crud-product-management](https://github.com/JyanesDev/mmeia-crud-product-management) |
| 02 | 🔐 Secure API | [mmeia-secure-task-api](https://github.com/JyanesDev/mmeia-secure-task-api) |
| 03 | 🏢 SaaS | [mmeia-multitenant-workspaces](https://github.com/JyanesDev/mmeia-multitenant-workspaces) |
| 04 | 🔌 MCP | **mmeia-notes-mcp-server** |
| 05 | 🤖 RAG | [mmeia-support-rag](https://github.com/JyanesDev/mmeia-support-rag) |

## 👨‍💻 Author

**Jonay Yanes** — [GitHub profile](https://github.com/JyanesDev)
