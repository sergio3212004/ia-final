# OptiLab API

## Inicio

```bash
python -m venv .venv
.venv/bin/pip install -r backend/requirements-dev.txt
.venv/bin/uvicorn backend.app.main:app --reload --port 8000
```

Documentación interactiva: `http://127.0.0.1:8000/docs`.

## Endpoints

- `GET /health`
- `POST /api/runs`
- `GET /api/runs/{run_id}`
- `POST /api/runs/{run_id}/step`
- `POST /api/runs/{run_id}/run`
- `POST /api/runs/{run_id}/pause`
- `POST /api/runs/{run_id}/stop`
- `GET /api/runs/{run_id}/events` (SSE)

El motor en `engine.py` no depende de FastAPI y puede probarse de forma aislada.

## Pruebas

```bash
.venv/bin/python -m unittest discover -s backend/tests -v
```
