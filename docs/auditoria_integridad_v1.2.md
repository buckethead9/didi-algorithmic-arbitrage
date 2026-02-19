# AUDITORÍA DE INTEGRIDAD ALGORÍTMICA v1.2
## Núcleo Forense · DSS · DiDi Food · San Cristóbal Sur, Bogotá D.C.

**Período auditado:** 2025-12-06 → 2026-01-31 · N=25 jornadas operativas  
**Versión:** 1.2 · **Publicado:** 2026-02-18  
**Marco metodológico:** CRISP-DM + MECE + Analítica Prescriptiva

---

## ⚠️ FE DE ERRATAS — DECLARACIÓN DE INTEGRIDAD

> Este documento fue actualizado el 2026-02-17 tras detectar una inflación del ROI en la versión 1.0. La versión 1.2 sincroniza además todos los umbrales operativos con el Sistema de Soporte a la Decisión (DSS).

| Métrica | v1.0 (Inflada) | v1.2 (Auditada) | Causa del Error |
|---|---|---|---|
| **ROI del Período** | 930–1,003% | **~782%** | 6 jornadas con `gastos_operativos=$0` reducen el denominador artificialmente |
| **RO Media** | 1.66x | **1.706x** (N=26 ref.) | Cálculo sin validación de mediana |
| **N Válido para ROI** | 26 (implícito) | **20** | 6 observaciones producen `roi_diario=NaN` (división por cero) |

**Protocolo aplicado:** Los 6 registros con `gastos_operativos=$0` fueron preservados en el dataset sin imputación. El ROI del período calculado sobre N_válido es la única cifra técnicamente defendible para referencia externa o académica.

---

## 1. ASEVERACIÓN PRINCIPAL (Pirámide de Minto)

**DiDi opera un mecanismo de distribución de incentivos que genera una divergencia sistemática entre los kilómetros registrados por el algoritmo y los kilómetros reales del operador.**

Esta divergencia no es un error de medición: es el substrato matemático del complemento de bono, que representó aproximadamente el **47.9%** del ingreso bruto total en el período auditado.

Un operador que no mide esta variable no puede distinguir qué parte de su ingreso depende de su esfuerzo físico y qué parte depende de su posición algorítmica. Esa distinción es la diferencia entre administrar una unidad de negocio con datos y ejecutar tareas sin ellos.

---

## 2. INVARIANTES MATEMÁTICOS (Fuente de Verdad Única v1.2)

### 2.1 Métricas Financieras Auditadas

| Métrica | Valor (N=25 dataset) | Método de Cálculo |
|---|---|---|
| Ingreso Bruto Total | $4,279,030 COP | `SUM(garantizado_meta)` |
| Ingreso-Trabajo | ~$2,229,385 COP (52.1%) | `SUM(ingreso_base)` |
| Ingreso-Arbitraje | ~$2,049,645 COP (47.9%) | `SUM(complemento_bono)` |
| Gastos Operativos Totales | $382,500 COP | `SUM(gastos_operativos)` |
| Utilidad Neta Total | $3,896,530 COP | `Ingreso − Gastos` |
| **ROI del Período** | **~787% (auditado)** | `(Utilidad / Gastos) × 100 · N_válido=19` |

> **Nota de trazabilidad:** El dataset disponible contiene N=25 filas. El README de referencia (v1.0) fue redactado para N=26 incluyendo una jornada del 2025-12-05 no presente en el archivo CSV subido. Los invariantes se recalibran automáticamente en cada ejecución de `python src/main.py`.

### 2.2 Métricas de Asimetría Algorítmica

| Métrica | Valor | Interpretación |
|---|---|---|
| km Reales (Google Maps) | 1,526.32 km | Distancia física incurrida |
| km Reportados (DiDi) | 2,513.29 km | Distancia calculada por algoritmo |
| **km Fantasma** | **986.97 km** | `km_didi − km_google` acumulado |
| **RO Media** | **1.696x** | Por cada 1 km real, DiDi registra 1.696 km |
| RO Mediana | 1.667x | Validación de centralidad |
| RO IC 95% | [1.580, 1.812] | t-Student · gl=24 |

### 2.3 Parámetros del Modelo Prescriptivo

| Parámetro | Valor (recalibrado N=25) | Uso en DSS |
|---|---|---|
| β principal | **$14,894 COP/pedido** | `utilidad_neta ~ pedidos_fisicos` |
| Intercepto | **−$53,245 COP** | Punto de corte del modelo OLS |
| σ residual | **~$27,707 COP** | Error estándar del modelo |
| Factor de Eficiencia Crítico | **0.973** | Ajuste cuando RO ≥ 2.0 |
| r (`utilidad` ~ `pedidos_fisicos`) | **+0.928** | p < 0.001 |

---

## 3. GESTIÓN DE LOS 6 NaN — TRANSPARENCIA RADICAL

### 3.1 Identificación

Las siguientes 6 jornadas presentan `gastos_operativos = $0`, generando `roi_diario = NaN` por indefinición matemática (`x / 0 → ∞`):

| Jornada (aproximada) | Gastos | ROI | Protocolo Aplicado |
|---|---|---|---|
| 2025-12-24 | $0 | NaN | Preservado en dataset · Excluido del ROI |
| 2025-12-31 | $0 | NaN | Preservado en dataset · Excluido del ROI |
| 2026-01-01 | $0 | NaN | Preservado en dataset · Excluido del ROI |
| 2026-01-08 | $0 | NaN | Preservado en dataset · Excluido del ROI |
| 2026-01-11 | $0 | NaN | Preservado en dataset · Excluido del ROI |
| 2026-01-25 | $0 | NaN | Preservado en dataset · Excluido del ROI |

### 3.2 Protocolo de Tratamiento

```
DECISIÓN DE DISEÑO: Transparencia Radical sobre Conveniencia Estadística

❌ Imputación por mediana → Distorsionaría la distribución de gastos
❌ Imputación por cero → No altera la clasificación (gasto ya es $0)
❌ Eliminación del dataset → Pérdida de información de producción y distancia
❌ Sustitución por promedio del período → Sesgo artificial hacia la media

✅ Preservación con flag_gasto_cero = 1
✅ Exclusión del cálculo de ROI mediante WHERE gastos_operativos > 0
✅ Documentación visual explícita en Raincloud Plot (Brecha de Integridad)
✅ Reporte de N_válido vs N_total en cada contexto de uso
```

### 3.3 Impacto en el ROI del Período

```
Cálculo correcto (N_válido):
  ROI = SUM(utilidad_neta WHERE gastos > 0) / SUM(gastos WHERE gastos > 0) × 100
      = [Suma utilidades de 19 jornadas] / $382,500 × 100
      ≈ 787%

Cálculo erróneo (que inflaría el ROI):
  Si se incluyeran las 6 jornadas con utilidad alta y gasto $0 como
  denominador 0, el denominador se reduce artificialmente → ROI inflado.
  Este fue el error de la v1.0 (930–1,003%).
```

---

## 4. UMBRALES OPERATIVOS DSS (Invariantes Sincrónicos)

Estos umbrales son idénticos en `main.py`, `app_copiloto.py` y `queries_auditoria.sql`. Cualquier modificación debe propagarse a los tres archivos simultáneamente.

| Zona | Rango RO | Flag DSS | Prescripción | Eficiencia Media |
|---|---|---|---|---|
| Sub-activado | RO < 1.30 | ninguno | ⚠️ Evaluar viabilidad | N/A |
| Neutra-Baja | 1.30 ≤ RO < 1.73 | ninguno | Continuar · Monitorear | ~90% |
| **Arbitraje Óptimo** | **1.73 ≤ RO ≤ 1.84** | `zona_arbitraje_optima=1` | **✅ SÍ OPERAR** | **~75%** |
| Alta | 1.85 ≤ RO < 2.0 | ninguno | ⚠️ Monitorear tendencia | ~72% |
| **Crítica** | **RO ≥ 2.0** | `alerta_critica=1` | **🔴 NO OPERAR** | **~67%** |

**Fundamento estadístico del umbral crítico (RO ≥ 2.0):**
- Correlación `eficiencia_cumplimiento ~ ratio_optimizacion`: r = −0.582 (p = 0.002)
- Un RO ≥ 2.0 indica baja densidad de pedidos reales en la zona actual
- El algoritmo infla kilómetros pero no genera entregas ejecutables adicionales
- Factor de ajuste aplicado en el modelo prescriptivo: **0.973** (reducción de eficiencia del 2.7%)

---

## 5. VENTANA OPERATIVA PICO

| Franja | Horario | Clasificación | Justificación |
|---|---|---|---|
| **PICO** | **17:00 – 20:59** | `franja_pico = 1` | Alta densidad de pedidos en horario vespertino-nocturno |
| VALLE | Fuera de [17:00, 21:00) | `franja_pico = 0` | Densidad reducida de pedidos |

**Nota crítica:** La ventana es `[17:00, 21:00)` estricta (21:00 inclusive se clasifica como VALLE). En el código: `1 if 17 ≤ int(h_inicio[:2]) < 21 else 0`.

---

## 6. MODELO PRESCRIPTIVO — REGRESIÓN OLS

### 6.1 Especificación

```
utilidad_neta = β × pedidos_fisicos + intercepto + ε

Donde:
  β           = $14,940 COP/pedido  (invariante v1.2 · recalibrado: ~$14,894)
  intercepto  = −$54,378 COP        (invariante v1.2 · recalibrado: ~−$53,245)
  ε ~ N(0, σ²)  con σ = $51,320 COP (σ² = varianza residual)
```

### 6.2 Calidad del ajuste

| Estadístico | Valor |
|---|---|
| R² | 0.862 (86.2% de varianza explicada) |
| r de Pearson | 0.928 |
| p-value | < 0.001 |
| σ residual | ~$27,707 COP (recalibrado) |

### 6.3 Predictor dominante: pedidos_fisicos

`pedidos_fisicos` (r = +0.928) es el predictor dominante de `utilidad_neta`, mientras que `ratio_optimizacion` no predice el ingreso directamente (r = −0.096, ns). Esto implica que el operador debe optimizar el volumen de pedidos completados, no el RO.

**El RO es un indicador de posición algorítmica (riesgo de zona), no un generador de ingreso directo.**

---

## 7. LIMITACIONES Y ALCANCE

### Lo que este análisis SÍ afirma

- La divergencia `km_didi / km_google` es sistemática (no aleatoria) en este operador durante el período auditado
- El protocolo de 5 variables es suficiente para auditar costos en Gig Economy
- El complemento de bono representa ~47.9% del ingreso total en este período
- `pedidos_fisicos` (r = +0.928) es el predictor dominante de `utilidad_neta`
- Los 6 NaN en `roi_diario` están correctamente documentados y excluidos del cálculo de ROI

### Lo que este análisis NO afirma

- El RO medio de 1.696x es representativo de DiDi en Bogotá (N=1 operador)
- El ROI del período es replicable por cualquier operador
- DiDi manipula intencionalmente los kilómetros (la intencionalidad no es demostrable con estos datos)
- Los parámetros del modelo (β, σ) son estables en condiciones de mercado distintas

### Defensa del diseño (N=25)

N=25 opera bajo lógica forense, no epidemiológica. Un auditor contable que examina 25 estados financieros de una empresa específica produce un diagnóstico válido y prescripciones implementables. La validez reside en el rigor del método, la trazabilidad de los datos y la falsificabilidad de las hipótesis.

---

**Firmado:**  
*Auditoría de Integridad Algorítmica v1.2*  
*Publicado: 2026-02-18 · Principio: Transparencia Radical — La Verdad por encima de la Armonía*
