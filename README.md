# OptiLab

Repositorio educativo para estudiar algoritmos genéticos, búsqueda tabú y colonia de hormigas mediante parámetros reproducibles, gráficos y logs estructurados.

La primera implementación funcional corresponde al algoritmo genético presentado en el material de clase: maximización de `f(x) = 1 - x²`, codificación binaria, selección por ruleta, cruce de un punto y mutación bit a bit.

## Estructura

- `src/components/`: componentes Vue del workspace.
- `src/composables/useGeneticLab.ts`: estado y coordinación de la interfaz.
- `src/services/api.ts`: cliente HTTP para Python.
- `backend/app/engine.py`: motor genético reproducible.
- `backend/app/main.py`: API FastAPI y eventos SSE.
- `backend/tests/`: pruebas del motor y endpoints.
- `docs/`: reglas funcionales y especificación basada en el material.

## Instalación

```bash
npm install
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements-dev.txt
```

## Desarrollo

Ejecutar en dos terminales:

```bash
npm run api
```

```bash
npm run dev
```

Frontend: `http://127.0.0.1:5173`

API: `http://127.0.0.1:8000`

Swagger: `http://127.0.0.1:8000/docs`

## Verificación

```bash
npm run test:backend
npm run build
```

La URL del backend puede cambiarse mediante `VITE_API_URL`.
