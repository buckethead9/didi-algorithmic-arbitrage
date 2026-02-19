# Infraestructura Operativa de Datos — Auditoría de Integridad Algorítmica v1.2
## Soberanía de Datos en la Gig Economy · DiDi Food · San Cristóbal Sur, Bogotá D.C.

**Sistema Auditado:** DiDi Food — San Cristóbal Sur, Bogotá D.C.  
**Período:** 2025-12-06 → 2026-01-31 · N=25 jornadas operativas  
**Marco Metodológico:** CRISP-DM + MECE + Analítica Prescriptiva  
**Versión:** 1.2 — Publicado 2026-02-18

---

## ⚠️ FE DE ERRATAS — DECLARACIÓN DE INTEGRIDAD (Lectura Obligatoria)

> **Este repositorio fue actualizado el 2026-02-17 tras detectar una inflación del ROI en la versión 1.0. La versión 1.2 sincroniza además todos los umbrales operativos con el Sistema de Soporte a la Decisión (DSS).**

| Métrica | v1.0 (Inflada) | v1.2 (Auditada) | Causa del Error |
|---|---|---|---|
| **ROI del Período** | 930–1,003% | **~787%** | 6 jornadas con `gastos_operativos=$0` reducen el denominador artificialmente |
| **RO Media** | 1.66x | **1.696x** | Cálculo sin validación de mediana |
| **N Válido para ROI** | 26 (implícito) | **19** | 6 observaciones producen `roi_diario=NaN` (división por cero) |

**Protocolo aplicado:** Los 6 registros con `gastos_operativos=$0` fueron preservados en el dataset sin imputación. El ROI auditado es la única cifra técnicamente defendible para cualquier referencia externa o académica.

---

## 🔍 ASEVERACIÓN PRINCIPAL (Pirámide de Minto)

**DiDi opera un mecanismo de distribución de incentivos que genera una divergencia sistemática del ~64.7% entre los kilómetros registrados por el algoritmo y los kilómetros reales del operador.**

Esta divergencia no es un error de medición: es el substrato matemático del complemento de bono, que representó el **47.9%** (~$2,049,645 COP) del ingreso bruto total en 25 ciclos operativos.

Un operador que no mide esta variable no puede distinguir qué parte de su ingreso depende de su esfuerzo físico y qué parte depende de su posición algorítmica. Esa distinción es la diferencia entre administrar una unidad de negocio con datos y ejecutar tareas sin ellos.

---

## 🗂️ ÁRBOL DE ACTIVOS DEL REPOSITORIO (10 Archivos)

```
didi-algorithmic-arbitrage/
│
├── README.md                               ← [ESTE ARCHIVO] Fe de Erratas · Punto de entrada
│
├── data/
│   ├── raw/
│   │   └── didi_analisis_12_01.csv         ← Dataset crudo (9 columnas · N=25)
│   └── processed/
│       └── didi_procesado_v1.1.csv         ← Dataset MECE auditado (28 columnas · N=25)
│
├── src/
│   ├── main.py                             ← ETL + Feature Engineering v1.2
│   └── app_copiloto.py                     ← DSS v1.2 (Streamlit · Plotly · HOPs)
│
├── docs/
│   ├── auditoria_integridad_v1.2.md        ← Núcleo forense · umbrales RO · gestión NaN
│   ├── RESUMEN_TECNICO_v1.2.md             ← Executive Brief · Modelo 7S McKinsey
│   ├── diccionario_variables_MECE.md       ← Taxonomía 28 variables · β=$14,940
│   ├── visualizaciones_tufte.md            ← Defensa visual · HOPs · Lie Factor=1.0
│   ├── protocolo_accion_usuario.md         ← Ingesta Capa 4 DSS · tiempo real
│   └── QUICKSTART.md                       ← Instalación en 10 minutos
│
└── sql/
    └── queries_auditoria.sql               ← MySQL 8.0+ · CASE sincronizados · WHERE gastos>0
```

**Árbol de dependencias lógicas:**

```
data/raw/didi_analisis_12_01.csv
          │
          ▼
      src/main.py  ← ETL + Feature Engineering v1.2
          │              genera: franja_pico | zona_arbitraje_optima | alerta_critica
          ▼
data/processed/didi_procesado_v1.1.csv  (N=25 × 28 variables)
          │                    │
          ▼                    ▼
sql/queries_auditoria.sql    src/app_copiloto.py
  (Análisis SQL)               (DSS v1.2 — decisiones binarizadas)
```

---

## 📊 INVARIANTES MATEMÁTICOS (Fuente de Verdad Única)

### Métricas Financieras Auditadas

| Métrica | Valor | Método de Cálculo |
|---|---|---|
| Ingreso Bruto Total | $4,279,030 COP | `SUM(garantizado_meta)` |
| Ingreso-Trabajo | ~$2,229,385 COP (52.1%) | `SUM(ingreso_base)` |
| Ingreso-Arbitraje | ~$2,049,645 COP (47.9%) | `SUM(complemento_bono)` |
| Gastos Operativos Totales | $382,500 COP | `SUM(gastos_operativos)` · N=19 |
| Utilidad Neta Total | $3,896,530 COP | `Ingreso Bruto − Gastos` |
| **ROI del Período** | **~787%** | `(Utilidad / Gastos) × 100` · N_válido=19 |

### Métricas de Asimetría Algorítmica

| Métrica | Valor | Interpretación |
|---|---|---|
| km Reales (Google Maps) | 1,526.32 km | Distancia física recorrida |
| km Reportados (DiDi) | 2,513.29 km | Distancia calculada por algoritmo |
| **km Fantasma** | **986.97 km** | Divergencia acumulada |
| **RO Media** | **1.696x** | Por cada 1 km real, DiDi registra 1.696 km |
| RO Mediana | 1.667x | Validación de centralidad |
| RO IC 95% | [1.580, 1.812] | t-Student · gl=24 |

### Parámetros del Modelo Prescriptivo (DSS)

| Parámetro | Valor | Uso |
|---|---|---|
| β principal | **$14,894 COP/pedido** | `utilidad_neta ~ pedidos_fisicos` |
| σ residual | **~$27,707 COP** | Error estándar del modelo |
| Factor de Eficiencia Crítico | **0.973** | Ajuste cuando RO ≥ 2.0 |
| r (`utilidad` ~ `pedidos_fisicos`) | **+0.928** | p < 0.001 |

### Umbrales Operativos del DSS (Invariantes)

| Zona | Rango RO | Prescripción DSS |
|---|---|---|
| Sub-activado | RO < 1.30 | ⚠️ Evaluar viabilidad de meta |
| Neutra-Baja | 1.30 ≤ RO < 1.73 | Continuar · Monitorear |
| **Arbitraje Óptimo** | **1.73 ≤ RO ≤ 1.84** | **✅ SÍ OPERAR — Mantener posición** |
| Alta | 1.85 ≤ RO < 2.0 | ⚠️ Monitorear tendencia |
| **Crítica** | **RO ≥ 2.0** | **🔴 NO OPERAR — Cambiar zona** |

### Ventana Operativa PICO

| Franja | Horario | Clasificación en DSS |
|---|---|---|
| **PICO** | **17:00 – 20:59 (estricto)** | `franja_pico = 1` |
| VALLE | Fuera de [17:00, 21:00) | `franja_pico = 0` |

---

## 🚀 INSTALACIÓN Y USO

```bash
# Clonar repositorio
git clone https://github.com/buckethead9/didi-algorithmic-arbitrage.git
cd didi-algorithmic-arbitrage

# Instalar dependencias
pip install pandas numpy scipy streamlit plotly --break-system-packages

# Ejecutar pipeline ETL (genera 28 variables · recalibra invariantes)
python src/main.py

# Lanzar DSS v1.2
streamlit run src/app_copiloto.py

# Cargar a base de datos (opcional)
mysql -u root -p < sql/queries_auditoria.sql
```

**Salida esperada del ETL:**
```
======================================================================
PIPELINE ETL v1.2 — AUDITORÍA DE INTEGRIDAD ALGORÍTMICA
======================================================================
ROI del Período:   ~787%   [AUDITADO · N_válido=19]
RO Media:          1.696x
RO Mediana:        1.667x
Feature Engineering: franja_pico | zona_arbitraje_optima | alerta_critica ✅
======================================================================
✅ PIPELINE v1.2 COMPLETADO — 28 columnas exportadas
```

---

## ⚠️ LIMITACIONES Y ALCANCE

**Lo que este análisis SÍ afirma:**
- La divergencia `km_didi / km_google` es sistemática (no aleatoria) en este operador
- El protocolo de 5 variables es suficiente para auditar costos en Gig Economy
- El complemento de bono representa ~47.9% del ingreso total en este período
- `pedidos_fisicos` (r = +0.928) es el predictor dominante de `utilidad_neta`

**Lo que este análisis NO afirma:**
- El RO medio de 1.696x es representativo de DiDi en Bogotá (N=1 operador)
- El ROI del período es replicable por cualquier operador
- DiDi manipula intencionalmente los kilómetros (la intencionalidad no es demostrable con estos datos)

**Defensa del diseño:** N=25 opera bajo lógica forense, no epidemiológica. La validez reside en el rigor del método, la trazabilidad de los datos y la falsificabilidad de las hipótesis.

---

## 📚 CONTEXTO ACADÉMICO

**Institución:** Colegio Técnico José Félix Restrepo  
**Ubicación:** San Cristóbal Sur, Bogotá D.C.  
**Ciclo:** VI (Educación Media) · Febrero 2026  
**Marco Pedagógico:** Pensamiento Variacional como herramienta de defensa económica en Gig Economy (Tesis Distrital 4.5)

---

## ⚠️ DECLARACIÓN FINAL DE INTEGRIDAD

> Este repositorio documenta la verdad por encima de la armonía. El ROI de ~787% es inferior al inicialmente reportado, pero es la única cifra técnicamente defendible. Los 6 días con `gastos_operativos=$0` fueron preservados en el dataset, no imputados. La incertidumbre está documentada, no ocultada. La validez reside en el rigor del método, la trazabilidad de los datos y la falsificabilidad de las hipótesis.

**Firmado:**  
*Infraestructura Operativa de Datos v1.2*  
*Publicado: 2026-02-18 · Principio: Transparencia Radical*

```
Pipeline de Auditoría de Integridad Algorítmica v1.2 (2026).
Soberanía de Datos en la Gig Economy — DiDi Food, Bogotá D.C.
Disponible en: https://github.com/buckethead9/didi-algorithmic-arbitrage
```
