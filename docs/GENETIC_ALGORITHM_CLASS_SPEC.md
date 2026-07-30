# Algoritmo genético — especificación basada en el material de clase

Fuentes analizadas:

- `/home/smonge/Downloads/AG- poster.png`
- `/home/smonge/Downloads/AG.pdf`
- `/home/smonge/Downloads/GuiaAG.docx`

## Flujo obligatorio

Cada generación sigue esta secuencia:

1. Representar/codificar la población.
2. Descodificar y evaluar la calidad de cada individuo.
3. Calcular probabilidades e intervalos de selección.
4. Seleccionar progenitores mediante ruleta.
5. Cruzar mediante corte de un punto.
6. Mutar bits de acuerdo con la probabilidad configurada.
7. Descodificar y evaluar la nueva población.
8. Reemplazar la población anterior.
9. Registrar el mejor individuo de la generación.
10. Verificar la condición de terminación.

La interfaz debe mostrar cada fase como un grupo de log expandible con su tabla asociada.

## Preset A — Ejemplo del póster

- Objetivo: maximizar `f(x) = 1 - x²`.
- Intervalo real: `[-1.00, 1.00]`.
- Precisión: dos decimales.
- Espacio discretizado esperado: 201 valores.
- Codificación empleada en la fuente: 8 bits.
- Población: 4 individuos.
- Selección: ruleta.
- Cruce: un punto.
- Probabilidad de mutación ilustrada: `0.10` por bit.
- Generación 0: aleatoria.

Fórmula de decodificación expuesta por el póster:

```text
x = [2 / (2^8 - 1)] × entero - 1
```

Población mostrada:

| Individuo | Cromosoma | Entero informado | x informado | Calidad informada |
| --- | --- | ---: | ---: | ---: |
| i1 | `10010100` | 148 | 0.161 | 0.974 |
| i2 | `10010001` | 145 | 0.137 | 0.981 |
| i3 | `00101001` | 41 | -0.678 | 0.540 |
| i4 | `01000101` | 69 en el póster / 65 en una tabla del PDF | -0.459 o -0.490 | 0.789 o 0.760 |

La aplicación no debe ocultar esta discrepancia. Debe calcular el entero directamente desde el cromosoma y marcar el valor de la fuente como “dato original con inconsistencia”.

Ejemplo de ruleta del póster:

| Individuo | Calidad | Probabilidad | Intervalo |
| --- | ---: | ---: | --- |
| i1 | 0.974 | 0.297 | `[0.000, 0.297)` |
| i2 | 0.981 | 0.299 | `[0.297, 0.596)` |
| i3 | 0.540 | 0.164 | `[0.596, 0.760)` |
| i4 | 0.789 | 0.240 | `[0.760, 1.000]` |

Números aleatorios ilustrados: `0.45` selecciona `i2`; `0.79` selecciona `i4`.

Cruce ilustrado:

- Padres: `i2 = 10010001` e `i4 = 01000101`.
- Punto de corte: 5.
- Descendientes: `10010101` y `01000001`.

Mutación ilustrada:

- `pm = 0.10`.
- Se evalúa cada bit.
- Si `random < pm`, el bit se invierte.

## Preset B — Guía de prueba de escritorio

- Objetivo: maximizar `f(x) = 1 - x²`.
- Intervalo real: `[-5.00, 5.00]`.
- Precisión: dos decimales.
- Codificación: entero desplazado.
- Transformación: `entero = x × 100 + 500`.
- Decodificación: `x = (entero - 500) / 100`.
- Valores codificados: `0..1000`.
- Longitud: 10 bits.
- Población inicial: `1.45`, `0.98`, `-1.25`, `-0.57`.
- Selección: ruleta.
- Cruce: un punto, elegido entre 9 cortes.
- Mutación ilustrada: `0.10` por bit.

### Tabla de evaluación inicial

| Individuo | Entero desplazado | Cromosoma | f(x) | Distancia a 1 | Aptitud `1/(1+d)` | Probabilidad | Intervalo |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1.45 | 645 | `1010000101` | -1.1025 | 2.1025 | 0.3223 | 0.1614 | `[0.0000, 0.1614)` |
| 0.98 | 598 | `1001010110` | 0.0396 | 0.9604 | 0.5101 | 0.2554 | `[0.1614, 0.4168)` |
| -1.25 | 375 | `0101110111` | -0.5625 | 1.4375 | 0.4103 | 0.2054 | `[0.4168, 0.6222)` |
| -0.57 | 443 | `0110111100` | 0.6751 | 0.3249 | 0.7548 | 0.3779 | `[0.6222, 1.0000]` |

Suma de aptitudes informada: `1.9975`.

Ejemplo: `random = 0.4789` selecciona el tercer individuo.

### Corte de un punto

- Para 10 bits existen 9 puntos de corte.
- La guía aproxima cada intervalo de corte a `1/9 ≈ 0.11`.
- `random = 0.7124` selecciona el séptimo punto.
- Deben mostrarse los segmentos de cada padre y los cromosomas resultantes.

### Resultado ilustrado después de mutación

| Cromosoma | Entero | x | f(x) |
| --- | ---: | ---: | ---: |
| `1010010111` | 663 | 1.63 | -1.6569 |
| `1000010111` | 535 | 0.35 | 0.8775 |
| `0101111111` | 383 | -1.17 | -0.3689 |
| `0010111111` | 191 | -3.09 | -8.5481 |

Mejor individuo ilustrado: `1000010111`, `x = 0.35`, `f(x) = 0.8775`.

## Parámetros editables de la web

### Problema y representación

- función objetivo;
- dirección: maximizar/minimizar;
- límite inferior y superior;
- precisión decimal;
- estrategia de codificación;
- longitud del cromosoma, calculada automáticamente y visible;
- validación de cromosomas fuera del dominio.

### Población

- tamaño;
- generación manual o aleatoria;
- individuos iniciales editables;
- semilla;
- política de reemplazo;
- elitismo.

### Selección

- método: ruleta, torneo o rango;
- cantidad de padres;
- normalización/escalado;
- números aleatorios automáticos o ingresados manualmente para prueba de escritorio.

### Cruce

- probabilidad de cruce;
- tipo: un punto, dos puntos o uniforme;
- punto de corte automático o manual;
- estrategia de emparejamiento.

### Mutación

- probabilidad por bit;
- modo aleatorio o randoms manuales;
- posiciones forzadas para demostración;
- límite de mutaciones por individuo, si aplica.

### Terminación

- máximo de generaciones;
- objetivo conocido opcional;
- generaciones sin mejora;
- botón de avance por fase y por generación.

## Salida y tablas por generación

Cada generación contiene las pestañas:

1. `Población y evaluación`
2. `Ruleta`
3. `Cruce`
4. `Mutación`
5. `Nueva población`
6. `Resumen`

Cada tabla debe permitir ver cálculo, fórmula sustituida, resultado, random utilizado y explicación. Los valores de entrada, calculados y copiados de la fuente se distinguen explícitamente.

El gráfico principal dibuja `f(x)=1-x²`, los individuos de la generación seleccionada como puntos sobre la curva y el mejor individuo con énfasis. Un gráfico secundario muestra mejor y promedio de aptitud por generación.

## Modo de validación de fuentes

La aplicación tiene dos modos:

- `Reproducir material`: conserva los números de la fuente y marca discrepancias.
- `Recalcular`: usa las fórmulas y la semilla como autoridad.

Un valor discrepante nunca se corrige silenciosamente.
