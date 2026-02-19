# RESUMEN TÉCNICO v1.2 — MODELO 7S McKINSEY
## Infraestructura Operativa de Datos · DiDi Food · San Cristóbal Sur, Bogotá D.C.

**Destinatarios:** Analistas de datos · Investigadores EdTech · Operadores de Gig Economy  
**Marco:** 7S McKinsey aplicado a la alineación de estrategia de datos y operación  
**Versión:** 1.2 · **Publicado:** 2026-02-18

---

## SÍNTESIS EJECUTIVA (Pirámide de Minto)

**Un operador de DiDi Food sin sistema de captura de datos no administra una unidad de negocio — ejecuta tareas por encargo.** La diferencia entre ambos estados es el acceso a 5 variables medibles, disponibles sin costo, que determinan si el 47.9% del ingreso bruto proviene de esfuerzo físico o de posición algorítmica.

Este repositorio demuestra que el Pensamiento Variacional — identificar variables, medir, calcular razones — es una herramienta de defensa económica concreta, no un concepto abstracto de la matemática escolar.

---

## 1. STRATEGY (Estrategia)

**Tesis:** Convertir la asimetría de información algorítmica en una ventaja operativa medible.

DiDi distribuye incentivos (complemento de bono) a través de un mecanismo que genera una divergencia sistemática entre los kilómetros registrados por el algoritmo (km_didi) y los kilómetros reales del operador (km_google). Esta divergencia, capturada como el Ratio de Optimización (RO = km_didi / km_google), determina qué fracción del ingreso proviene de la posición algorítmica versus el esfuerzo físico.

**Prescripción estratégica:** El operador debe maximizar `pedidos_fisicos` (predictor dominante, r=0.928) mientras mantiene el RO en la zona óptima [1.73–1.84], donde la utilidad media es máxima sin el colapso de eficiencia que ocurre en RO ≥ 2.0.

---

## 2. STRUCTURE (Estructura del Sistema)

**Arquitectura de 4 capas del DSS:**

```
Capa 1: Captura de Datos Primarios
  Instrumentos: Google Maps · DiDi App · Registro manual del operador
  Variables: fecha · h_inicio · h_fin · km_google · km_didi · ingreso_bruto
             pedidos_cohete · pedidos_normales · gasto_extra

Capa 2: ETL y Feature Engineering
  Herramienta: src/main.py (Python 3.x · pandas · numpy · scipy)
  Salida: didi_procesado_v1.1.csv (N × 28 variables MECE)
  Features: franja_pico | zona_arbitraje_optima | alerta_critica

Capa 3: Almacenamiento y Análisis SQL
  Herramienta: sql/queries_auditoria.sql (MySQL 8.0+)
  Funciones: clasificación operativa · ROI auditado · análisis de sensibilidad

Capa 4: DSS — Decisión Binarizada en Tiempo Real
  Herramienta: src/app_copiloto.py (Streamlit + Plotly)
  Salida: [SÍ OPERAR / NO OPERAR] basado en 5 variables de ingesta
  Visualización: HOPs · Patrón Z · Paleta semántica Tufte
```

---

## 3. SYSTEMS (Sistemas y Procesos)

### Pipeline de Recalibración N+1

```
Jornada N+1 completada
        ↓
Operador registra 9 variables en CSV raw
(fecha · h_inicio · h_fin · km_google · km_didi ·
 ingreso_bruto · pedidos_cohete · pedidos_normales · gasto_extra)
        ↓
python src/main.py
        ↓
Recalibración automática de:
  - ROI del período  - RO media/mediana
  - β del modelo     - σ residual
  - r de Pearson     - IC 95% para RO
        ↓
didi_procesado_v1.1.csv actualizado (28 variables × N+1)
        ↓
streamlit run src/app_copiloto.py
        ↓
DSS v1.2 con invariantes recalibrados disponible para la siguiente jornada
```

### Protocolo de Integridad de Datos

1. **No imputación:** Los 6 valores `NaN` en `roi_diario` se preservan como `NaN`, no se reemplazan
2. **No eliminación de outliers:** Todos los N=25 registros permanecen en el dataset
3. **Validación cruzada de km_google:** Verificado contra historial GPS del dispositivo
4. **Trazabilidad completa:** Cada valor derivado tiene fórmula documentada en `diccionario_variables_MECE.md`

---

## 4. SHARED VALUES (Valores Compartidos)

**Transparencia Radical sobre Armonía Estadística**

El ROI de la versión v1.2 (~787%) es inferior al reportado en la v1.0 (930–1,003%), pero es la única cifra técnicamente defendible. La corrección se documenta públicamente en la Fe de Erratas del README.

**Principios operativos del sistema:**
- Outliers eliminados: **0** (transparencia total de la muestra)
- Valores imputados: **0** (los NaN permanecen como NaN)
- Fuentes independientes: `km_google` verificado independientemente de `km_didi`
- Falsificabilidad: todas las hipótesis son verificables con datos adicionales

---

## 5. SKILLS (Competencias Técnicas)

### Competencias del pipeline (src/main.py)

| Módulo | Técnica | Herramienta |
|---|---|---|
| Ingesta y validación | Esquema de columnas requeridas | pandas · Python |
| Tratamiento de medianoche | Adición condicional de 1440 minutos | Aritmética de tiempo |
| Feature Engineering | Reglas de negocio binarizadas | pandas vectorizado |
| Separación MECE | Descomposición de ingreso bruto | Álgebra lineal simple |
| Regresión OLS | Mínimos cuadrados ordinarios | scipy.stats.linregress |
| IC 95% (RO) | Distribución t-Student | scipy.stats.t.interval |
| Recalibración N+1 | Recálculo completo en cada ejecución | Stateless pipeline |

### Competencias del DSS (src/app_copiloto.py)

| Módulo | Técnica | Herramienta |
|---|---|---|
| HOPs | Simulación Monte Carlo (50 trayectorias) | numpy.random.normal |
| Visualización | Principios de Edward Tufte | Plotly + CSS custom |
| Decisión binarizada | Árbol de reglas deterministas | Python condicional |
| Caché de datos | Memoización con TTL=300s | @st.cache_data |
| Layout Patrón Z | Columnas y tabs jerarquizados | Streamlit layout |

---

## 6. STAFF (Capacidad de Replicación)

### Barrera de entrada para nuevos operadores

La implementación completa del DSS v1.2 requiere:

1. **Captura manual:** 9 variables por jornada · ~5 minutos post-jornada
2. **Hardware:** Smartphone con Google Maps (verificación de km)
3. **Software:** Python 3.x (instalable gratuitamente) · Editor de texto básico
4. **Conocimiento previo:** Capacidad de leer números enteros y decimales

**Tesis validada (aplicación EdTech):** La barrera para el análisis de costos en emprendimiento no es aritmética. El cálculo de rentabilidad real requiere cinco variables y una división. La barrera es la ausencia de un sistema de captura de datos.

---

## 7. STYLE (Estilo de Comunicación)

El DSS v1.2 comunica prescripciones, no reportes. Cada visualización tiene un título-aseveración (Pirámide de Minto), no un título descriptivo. El panel de decisión entrega exactamente dos respuestas posibles: **SÍ OPERAR** o **NO OPERAR**.

Este estilo es apropiado para operadores que tienen minutos, no horas, para procesar información antes de una jornada. La carga cognitiva del análisis recae en el sistema, no en el usuario.

---

## MÉTRICAS CLAVE DEL PERÍODO (Invariantes v1.2)

| Métrica | Valor |
|---|---|
| Ingreso Bruto Total | $4,279,030 COP |
| ROI Auditado del Período | ~787% (N_válido=19) |
| RO Media | 1.696x |
| km Fantasma Total | 986.97 km |
| β Modelo | $14,894 COP/pedido |
| r (pedidos → utilidad) | 0.928 (p < 0.001) |
| Predictor dominante | `pedidos_fisicos` |
| Zona óptima RO | [1.73, 1.84] |
| Umbral crítico RO | ≥ 2.0 |

---

**Firmado:**  
*Resumen Técnico v1.2 · Infraestructura Operativa de Datos*  
*Colegio Técnico José Félix Restrepo · San Cristóbal Sur · Bogotá D.C. · Febrero 2026*
