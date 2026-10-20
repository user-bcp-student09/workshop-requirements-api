# Workshop Requirements API — Python FastAPI

> **Laboratorio intencionalmente vulnerable.** Ejecutar únicamente en local, repositorios privados y ambientes aislados. No publicar en Internet ni desplegar en CERT/PROD.

API FastAPI que administra tareas del workshop y recibe archivos de requerimientos. Usa SQLite y consume el token emitido por el backend Quarkus.

## Ejecución

Requisitos: Python 3.13.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Swagger: `http://localhost:8000/docs`

La API valida el JWT HS256 emitido por el backend de autenticación. Configura
el mismo valor de `AUTH_JWT_SECRET` en ambos servicios; la API no arranca si
falta o tiene menos de 32 bytes.
Las solicitudes sin un token válido reciben HTTP `401` con
`{"detail":"ocurrio un error"}`.

## Endpoints

- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/summary`
- `POST /api/requirements`
- `GET /api/backend-health`

La rama `main` contiene autenticación débil, SQL concatenado, manejo inseguro de nombres de archivo, conexión global, lógica monolítica y dependencias con CVEs.
