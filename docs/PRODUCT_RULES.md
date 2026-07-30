# OptiLab — Diseño funcional y reglas

## Objetivo

Construir un repositorio educativo para ejecutar, observar y comparar:

1. Algoritmos genéticos.
2. Búsqueda tabú.
3. Colonia de hormigas.

La prioridad es la trazabilidad pedagógica. Cada resultado debe poder explicarse reconstruyendo sus pasos desde los logs.

## Arquitectura propuesta

- Frontend: Vue 3 + TypeScript + Vite.
- Backend: Python con una API HTTP y canal de eventos en tiempo real (SSE como primera opción; WebSocket solo si se requiere control bidireccional continuo).
- Motor: módulos Python independientes para `genetic`, `tabu` y `ant_colony`.
- Persistencia inicial: SQLite para ejecuciones, parámetros, métricas y eventos.
- Gráficos: librería compatible con Vue; recibe series normalizadas desde el backend.

El navegador nunca implementa la lógica del algoritmo. Solo configura ejecuciones, envía comandos, consume eventos y presenta resultados.

## Contrato común de ejecución

Toda ejecución debe tener:

- `run_id` único.
- `algorithm`: `genetic`, `tabu` o `ant_colony`.
- `problem_type` y datos de entrada.
- `optimization_direction`: `minimize` o `maximize`.
- `seed` explícita.
- parámetros validados y guardados.
- fecha de inicio y finalización.
- estado: `queued`, `running`, `paused`, `completed`, `stopped` o `failed`.
- mejor solución, mejor objetivo, iteración de hallazgo, total de evaluaciones y duración.
- versión del algoritmo para reproducibilidad.

## Contrato de logs

Cada evento se emite como dato estructurado, no como texto libre:

```json
{
  "event_id": 42,
  "run_id": "run_2026_001",
  "timestamp": "2026-07-30T10:15:32.120-05:00",
  "algorithm": "genetic",
  "level": "info",
  "phase": "selection",
  "step_type": "generation",
  "step": 7,
  "operation": "tournament_selection",
  "objective_current": 128.4,
  "objective_best": 121.9,
  "inputs": {},
  "outputs": {},
  "explanation": "Se seleccionaron los padres mediante torneo de tamaño 3."
}
```

Reglas:

- `event_id` crece de forma monotónica dentro de la ejecución.
- `step` identifica generación o iteración según el algoritmo.
- `explanation` debe ser comprensible sin leer el código.
- Los objetos grandes se resumen en el evento y se guardan como artefactos referenciados.
- Los errores conservan contexto, traceback técnico y una explicación amigable separada.
- Los logs son inmutables y exportables en JSON/CSV.

## Eventos mínimos por algoritmo

### Genético

- inicialización de población;
- evaluación de cada individuo o resumen de evaluación;
- selección;
- cruce, indicando padres y descendencia;
- mutación, indicando posiciones/genes afectados;
- reemplazo o elitismo;
- resumen de generación;
- criterio de parada.

Métricas: mejor, promedio y peor fitness; diversidad; evaluaciones; tasa efectiva de mutación.

### Tabú

- solución inicial;
- generación del vecindario;
- evaluación de movimientos candidatos;
- descarte por condición tabú;
- aplicación de aspiración;
- selección del mejor movimiento admisible;
- actualización de lista tabú;
- resumen de iteración;
- criterio de parada.

Métricas: objetivo actual, mejor global, tamaño de vecindario, movimientos tabú, aspiraciones y tenencia restante.

### Colonia de hormigas

- inicialización de feromonas;
- inicio de hormiga;
- probabilidades de transición;
- elección de siguiente componente;
- solución construida por hormiga;
- evaluación;
- evaporación;
- depósito de feromonas;
- resumen de iteración;
- criterio de parada.

Métricas: mejor, promedio y peor objetivo de colonia; niveles de feromona; evaporación; evaluaciones.

## Gráfico de función objetivo

- Eje X: generación o iteración.
- Eje Y: valor de la función objetivo, con dirección visible.
- Serie obligatoria: mejor valor acumulado.
- Serie obligatoria: valor actual o mejor del paso.
- Serie opcional: promedio de población/colonia.
- Cada punto guarda `event_id` o rango de eventos relacionado.
- Hover muestra paso, objetivo, mejora, tiempo y resumen de operación.
- Clic en el punto lleva al grupo de logs correspondiente.
- Clic en un log resalta el punto.
- Debe existir tabla textual equivalente para accesibilidad y exportación.

## Prueba de escritorio

La aplicación permite cuatro modos:

1. Ejecución completa.
2. Pausar/reanudar.
3. Avanzar un paso pedagógico.
4. Reproducir una ejecución guardada sin recalcular.

Unidad de “paso”:

- Genético: una generación completa.
- Tabú: una iteración con elección y actualización tabú.
- Hormigas: una iteración completa de la colonia.

Dentro del paso, el log conserva suboperaciones expandibles.

## Validación

- Tipos, rangos y obligatoriedad se validan en frontend y backend.
- El backend es la autoridad final.
- La semilla es obligatoria; si se genera automáticamente, se muestra antes de ejecutar.
- No se permite iniciar con población, vecindario o colonia vacía.
- Los criterios de parada deben incluir al menos un límite finito.
- `NaN`, infinito o soluciones inválidas detienen la ejecución con evento de error.
- Nunca se declara “óptimo global” sin evidencia externa configurada.

## Pantallas

- Dashboard.
- Workspace reutilizable por algoritmo.
- Historial de ejecuciones.
- Detalle/reproducción de ejecución.
- Comparador de dos o más ejecuciones.
- Guía de conceptos y parámetros.

## Criterios de aceptación de la primera entrega

- Los tres algoritmos aparecen en navegación y pueden recibir configuraciones independientes.
- Una ejecución Python transmite eventos visibles sin recargar.
- El usuario puede pausar y avanzar paso a paso.
- El gráfico se actualiza y está sincronizado con el log.
- La misma semilla y parámetros reproducen el mismo resultado bajo la misma versión.
- Una ejecución se puede exportar e importar.
- Estados vacíos, errores y desconexión del backend tienen tratamiento visible.
- Todas las funciones principales son utilizables en 360px de ancho sin depender de hover.
- La selección de generación, fase y log se conserva al cambiar entre escritorio y móvil.

## Material de clase incorporado

La especificación detallada del primer algoritmo se encuentra en
`docs/GENETIC_ALGORITHM_CLASS_SPEC.md`.

Para el algoritmo genético, la primera entrega debe incluir:

- los presets “Ejemplo del póster” y “Guía de prueba de escritorio”;
- codificación binaria de 8 y 10 bits según el preset;
- selección por ruleta con probabilidades e intervalos;
- cruce de un punto con corte visible;
- mutación evaluada bit por bit;
- tablas completas por fase y generación;
- gráfico de `f(x)=1-x²` con los individuos como puntos;
- modo “Reproducir material” y modo “Recalcular”;
- alertas de discrepancia cuando el material no coincide con el cálculo.

## Reglas responsivas

- Escritorio: parámetros, visualizaciones/tablas y logs pueden mostrarse simultáneamente.
- Tablet: parámetros en panel lateral desplegable; contenido principal en dos columnas; logs debajo.
- Móvil: navegación inferior y selector `Gráfico / Tabla / Pasos / Logs`.
- Las tablas se representan como tarjetas de datos legibles; la tabla original queda disponible con desplazamiento horizontal.
- Los controles de ejecución son adhesivos y tienen áreas táctiles mínimas de 44×44 px.
- Los gráficos aceptan toque, tienen alternativa tabular y no requieren hover.
- Los parámetros se agrupan en acordeones con resumen de valores.
- La experiencia móvil permite configurar y ejecutar, no es únicamente de consulta.
- Se prueban como mínimo los anchos 360, 390, 768, 1024 y 1440 px.
