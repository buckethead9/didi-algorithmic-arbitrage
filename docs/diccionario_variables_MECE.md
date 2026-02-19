# DICCIONARIO DE VARIABLES — PRINCIPIO MECE
## Sistema de Soporte a la Decisión — DiDi Food · Gig Economy

**Versión:** 1.2  
**Principio:** Mutually Exclusive · Collectively Exhaustive (MECE)  
**Actualizado:** 2026-02-18  
**Constante β:** $14,940 COP/pedido · **σ residual:** $51,320 COP  
**Zona Óptima:** 1.73 ≤ RO ≤ 1.84 · **Zona Crítica:** RO ≥ 2.0

---

## TAXONOMÍA COMPLETA (N=28 variables · 6 dimensiones · sin solapamientos)

```
UNIVERSO DE VARIABLES (N=28)
│
├── DIMENSIÓN 1: TIEMPO-IDENTIFICACIÓN (5 variables)
│   ├── fecha              [Primaria — Identificador temporal]
│   ├── h_inicio           [Primaria — Timestamp inicio · formato HH:MM]
│   ├── h_fin              [Primaria — Timestamp fin · formato HH:MM]
│   ├── duracion_horas     [Derivada — Con tratamiento de medianoche]
│   └── franja_pico        [Feature Engineering · 1 si 17:00 ≤ h_inicio < 21:00]
│
├── DIMENSIÓN 2: DISTANCIA (4 variables)
│   ├── km_google          [Primaria — Fuente independiente del algoritmo]
│   ├── km_didi            [Primaria — Fuente algorítmica]
│   ├── km_fantasma        [Derivada = km_didi − km_google]
│   └── ratio_optimizacion [Derivada = km_didi ÷ km_google · RO]
│
├── DIMENSIÓN 3: INGRESO — SEPARACIÓN MECE (4 variables)
│   ├── ingreso_base       [Primaria — Ingreso-Trabajo]
│   ├── complemento_bono   [Primaria — Ingreso-Arbitraje]
│   ├── garantizado_meta   [Derivada = ingreso_base + complemento_bono]
│   └── proporcion_bono    [Derivada = complemento_bono ÷ garantizado_meta]
│
├── DIMENSIÓN 4: COSTO E INTEGRIDAD (2 variables)
│   ├── gastos_operativos  [Primaria — Costo verificable]
│   └── flag_gasto_cero    [Bandera = 1 si gastos = 0]
│
├── DIMENSIÓN 5: RESULTADO (5 variables)
│   ├── utilidad_neta      [Derivada = garantizado_meta − gastos_operativos]
│   ├── utilidad_por_hora  [Ratio = utilidad_neta ÷ duracion_horas]
│   ├── roi_diario         [Ratio = (utilidad_neta ÷ gastos) × 100 · NaN si gastos=0]
│   └── rentabilidad_binaria [Bandera = 1 si utilidad_neta > 0]
│
├── DIMENSIÓN 6: PRODUCCIÓN Y EFICIENCIA (7 variables)
│   ├── pedidos_fisicos    [Primaria — Unidad de producción · Predictor β]
│   ├── unidades_progreso  [Primaria — Contabilización DiDi]
│   ├── eficiencia_cumplimiento [Derivada = unidades_progreso ÷ pedidos_fisicos]
│   ├── km_por_pedido_google    [Ratio = km_google ÷ pedidos_fisicos]
│   ├── km_por_pedido_didi      [Ratio = km_didi ÷ pedidos_fisicos]
│   ├── ingreso_por_km_google   [Ratio = garantizado_meta ÷ km_google]
│   └── ingreso_por_hora        [Ratio = garantizado_meta ÷ duracion_horas]
│
└── DIMENSIÓN 7: FEATURE ENGINEERING DSS (3 variables · generadas por main.py v1.2)
    ├── franja_pico            [1 si h_inicio ∈ [17:00, 21:00) · 0 si VALLE]
    ├── zona_arbitraje_optima  [1 si 1.73 ≤ RO ≤ 1.84 · 0 en otro caso]
    └── alerta_critica         [1 si RO ≥ 2.0 · 0 en otro caso]
```

---

## DIMENSIÓN 1: TIEMPO-IDENTIFICACIÓN

### `fecha`
| Atributo | Especificación |
|----------|----------------|
| **Tipo** | DATE |
| **Formato** | YYYY-MM-DD |
| **Fuente** | Registro del operador |
| **Rango** | 2025-12-05 → 2026-01-31 |
| **N** | 26 jornadas (45.6% de cobertura del período de 57 días) |

---

### `h_inicio` y `h_fin`
| Atributo | Especificación |
|----------|----------------|
| **Tipo** | STRING |
| **Formato** | `HH:MM` (24 horas) — ejemplo: `"17:01"`, `"00:12"` |
| **Fuente** | Timestamp de activación/desactivación en DiDi App |
| **Tratamiento especial** | Cruces de medianoche: si `h_fin < h_inicio` → agregar 24 h |

> **Estándar de formato:** Los tiempos se almacenan como strings `HH:MM`, no como decimales. Ejemplo correcto: `"08:31"`. Ejemplo incorrecto: `8.52`.

**Jornadas con cruce de medianoche:** 4 registros detectados. Tratamiento: `minutos_fin += 1440`.

---

### `duracion_horas`
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `calcular_duracion_turno(h_inicio, h_fin)` |
| **Tipo** | DECIMAL(5,2) |
| **Unidad** | Horas |
| **Total acumulado** | 236.72 h |
| **Promedio** | 9.10 h/jornada |
| **Rango** | 0.82 h — 12.73 h |

---

### `franja_pico` ← Feature Engineering DSS
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `1 si 17 ≤ int(h_inicio[:2]) < 21, else 0` |
| **Tipo** | INTEGER (0 o 1) |
| **Ventana PICO** | **Estrictamente 17:00 — 20:59** (4 horas exactas) |
| **Fundamentación** | Alta densidad de pedidos en horario vespertino-nocturno |
| **Uso en DSS** | Factor de priorización en el panel de decisión |

> **Nota crítica:** La ventana PICO es `[17:00, 21:00)` estricta. Las 21:00 en adelante se clasifican como VALLE.

---

## DIMENSIÓN 2: DISTANCIA

### `km_google` — Distancia Física Real
| Atributo | Especificación |
|----------|----------------|
| **Tipo** | DECIMAL(8,2) |
| **Fuente** | Google Maps / Historial de ubicaciones GPS — **independiente de DiDi** |
| **Naturaleza** | Distancia euclidea real recorrida |
| **Unidad** | Kilómetros |
| **Limpieza aplicada** | `"45,06 km"` → `45.06` |
| **Total acumulado** | 1,571.38 km |
| **Media** | 60.44 km/jornada |
| **Rango** | 18.79 — 104.61 km/jornada |

`km_google` es la **distancia física real** que incurre en costos verificables (combustible, desgaste, tiempo). Es el denominador del RO y la referencia del mundo físico.

---

### `km_didi` — Distancia Percibida por el Algoritmo
| Atributo | Especificación |
|----------|----------------|
| **Tipo** | DECIMAL(8,2) |
| **Fuente** | App DiDi — pantalla de resumen de jornada |
| **Naturaleza** | Distancia calculada por el algoritmo interno de DiDi |
| **Unidad** | Kilómetros |
| **Limpieza aplicada** | `"88,6 km"` → `88.6` |
| **Total acumulado** | 2,601.89 km |
| **Media** | 100.07 km/jornada |
| **Rango** | 25.8 — 151.3 km/jornada |

`km_didi` es el **numerador del RO** y la base de cálculo del `complemento_bono`. La diferencia entre `km_didi` y `km_google` no representa un error de medición: es el substrato matemático del Ingreso-Arbitraje.

---

### `km_fantasma`
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `km_fantasma = km_didi − km_google` |
| **Tipo** | DECIMAL(8,2) · siempre ≥ 0 en dataset |
| **Unidad** | Kilómetros |
| **Total acumulado** | **1,030.51 km** |
| **Promedio/jornada** | 39.63 km |

Kilómetros no recorridos físicamente pero contabilizados por DiDi para el cálculo del bono.

---

### `ratio_optimizacion` (RO) — Métrica Central de Asimetría
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `RO = km_didi ÷ km_google` |
| **Tipo** | DECIMAL(4,2) |
| **Unidad** | Factor multiplicador (adimensional) |
| **Media auditada** | **1.706** |
| **Mediana** | **1.700** |
| **Desv. Estándar** | 0.279 |
| **IC 95%** | [1.594, 1.818] |
| **Rango** | 1.170 — 2.370 |

**Tabla de umbrales operativos (invariantes del DSS):**

| Rango RO | Zona | `zona_arbitraje_optima` | `alerta_critica` | Prescripción |
|----------|------|------------------------|-----------------|--------------|
| RO < 1.30 | Sub-activado | 0 | 0 | ⚠️ Evaluar viabilidad |
| 1.30 ≤ RO < 1.73 | Neutra-Baja | 0 | 0 | Continuar · Monitorear |
| **1.73 ≤ RO ≤ 1.84** | **Arbitraje Óptimo** | **1** | **0** | **✅ SÍ OPERAR** |
| 1.85 ≤ RO < 2.0 | Alta | 0 | 0 | ⚠️ Monitorear tendencia |
| **RO ≥ 2.0** | **Crítica** | **0** | **1** | **🔴 NO OPERAR** |

**Correlación con otras variables:**
- `utilidad_neta`: r = −0.096 (p = 0.641, ns) — **El RO no predice el ingreso**
- `eficiencia_cumplimiento`: r = −0.582 (p = 0.002) — Fundamento del umbral crítico RO ≥ 2.0

---

## DIMENSIÓN 3: INGRESO — SEPARACIÓN MECE

**Principio de separación:**

$$Ingreso\_Bruto = \underbrace{ingreso\_base}_{\text{Ingreso-Trabajo}} + \underbrace{complemento\_bono}_{\text{Ingreso-Arbitraje}}$$

Las dos categorías son **mutuamente excluyentes** (cada peso pertenece a una sola) y **colectivamente exhaustivas** (su suma es el ingreso bruto total).

---

### `ingreso_base` — Ingreso-Trabajo
| Atributo | Especificación |
|----------|----------------|
| **Tipo** | INTEGER · COP |
| **Fuente** | App DiDi — pantalla de resumen |
| **Dependencia** | Requiere km reales + tiempo + pedidos físicos |
| **Total acumulado** | $2,299,070 COP (52.1% del bruto) |
| **Promedio/jornada** | $88,426 COP |

---

### `complemento_bono` — Ingreso-Arbitraje
| Atributo | Especificación |
|----------|----------------|
| **Tipo** | INTEGER · COP |
| **Fuente** | App DiDi — bono del día |
| **Dependencia** | Requiere posición algorítmica favorable (RO > 1.0) + cumplimiento de meta |
| **Total acumulado** | $2,109,960 COP (47.9% del bruto) |
| **Promedio/jornada** | $81,152 COP |

---

### `garantizado_meta`
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `garantizado_meta = ingreso_base + complemento_bono` |
| **Tipo** | INTEGER · COP |
| **Total acumulado** | $4,409,030 COP |
| **Promedio/jornada** | $169,578 COP |

---

### `proporcion_bono`
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `proporcion_bono = complemento_bono ÷ garantizado_meta` |
| **Tipo** | DECIMAL(4,2) |
| **Media** | **0.479** (47.9%) |
| **IC 95%** | [0.410, 0.500] |
| **Rango** | 0.186 — 0.634 |
| **Umbral crítico DSS** | **< 0.30** → Bono sub-activado |

---

## DIMENSIÓN 4: COSTO E INTEGRIDAD

### `gastos_operativos`
| Atributo | Especificación |
|----------|----------------|
| **Tipo** | INTEGER · COP · DEFAULT 0 |
| **Fuente** | Registro manual del operador (recibos, transacciones) |
| **Total acumulado** | $399,500 COP (20 jornadas con gasto > $0) |
| **Promedio** (solo jornadas con gasto > $0) | $19,975 COP/jornada |
| **Jornadas con gasto $0** | **6 (23.1%)** → `roi_diario = NaN` |

---

### `flag_gasto_cero`
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `1 if gastos_operativos == 0 else 0` |
| **Tipo** | INTEGER (0 o 1) |
| **N con flag = 1** | 6 jornadas |
| **Uso** | Filtro para cálculo de ROI auditado · `WHERE gastos_operativos > 0` |

---

## DIMENSIÓN 5: RESULTADO

### `utilidad_neta`
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `utilidad_neta = garantizado_meta − gastos_operativos` |
| **Tipo** | INTEGER · COP |
| **Total acumulado** | $4,009,530 COP |
| **Promedio/jornada** | $154,212 COP · IC 95%: [$128,345, $180,079] |

**Predictor dominante:** `pedidos_fisicos` (r = +0.929, p < 0.001, constante β = **$14,940 COP/pedido**)

---

### `roi_diario`
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `(utilidad_neta ÷ gastos_operativos) × 100` si `gastos > 0` |
| **Tipo** | DECIMAL(8,2) · `NaN` si `gastos = 0` |
| **N válido** | **20** (6 tienen `NaN`) |
| **ROI del período auditado** | **782.24%** |

> `roi_diario = NaN` significa **indefinido matemáticamente**, no infinito. Las 6 jornadas con `NaN` se excluyen del cálculo de ROI del período pero se preservan en el dataset.

---

## DIMENSIÓN 6: PRODUCCIÓN Y EFICIENCIA

### `pedidos_fisicos` — Predictor Dominante (Constante β)
| Atributo | Especificación |
|----------|----------------|
| **Tipo** | INTEGER |
| **Fuente** | Conteo manual del operador |
| **Total acumulado** | 363 pedidos |
| **Promedio/jornada** | 13.96 pedidos |
| **Rango** | 3 — 21 pedidos |
| **Correlación con `utilidad_neta`** | r = **+0.929** · p < 0.001 |
| **Constante β en DSS** | **$14,940 COP por pedido adicional** |
| **σ residual** | **$51,320 COP** |

El modelo prescriptivo del DSS usa `pedidos_fisicos` como variable predictora principal:

```
utilidad_esperada = β × pedidos_input + intercepto
                  = $14,940 × N + intercepto
Rango de confianza (IC 90%) = [P5, P95] de 50 trayectorias con σ = $51,320
```

---

### `eficiencia_cumplimiento`
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `unidades_progreso ÷ pedidos_fisicos` |
| **Tipo** | DECIMAL(4,2) |
| **Media** | 0.901 |
| **Rango** | 0.500 — 1.200 |
| **Correlación con RO** | r = **−0.582** · p = 0.002 → Fundamento del umbral crítico RO ≥ 2.0 |

---

## DIMENSIÓN 7: FEATURE ENGINEERING DSS (generadas por main.py v1.2)

### `franja_pico`
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `1 if 17 ≤ int(h_inicio[:2]) < 21 else 0` |
| **Tipo** | INTEGER (0 o 1) |
| **Ventana PICO** | Estrictamente `[17:00, 21:00)` |
| **Uso en DSS** | Factor de priorización · Filtro de franja horaria en sidebar |

### `zona_arbitraje_optima`
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `1 if 1.73 ≤ ratio_optimizacion ≤ 1.84 else 0` |
| **Tipo** | INTEGER (0 o 1) |
| **Fundamentación** | Q3 de cuartiles RO · Utilidad media máxima: $211,250 COP |
| **Uso en DSS** | Activa panel ✅ SÍ OPERAR |

### `alerta_critica`
| Atributo | Especificación |
|----------|----------------|
| **Fórmula** | `1 if ratio_optimizacion >= 2.0 else 0` |
| **Tipo** | INTEGER (0 o 1) |
| **Fundamentación** | Eficiencia de cumplimiento colapsa a 73.0% · r(RO, efic) = −0.582 |
| **Factor de eficiencia** | **0.973** — ajuste aplicado en modelo prescriptivo cuando `alerta_critica = 1` |
| **Uso en DSS** | Activa panel 🔴 NO OPERAR |

---

## VALIDACIÓN DEL PRINCIPIO MECE

### Exclusividad Mutua (Mutually Exclusive)

| Par de Categorías | Verificación |
|-------------------|--------------|
| `ingreso_base` vs `complemento_bono` | ✅ `ingreso_base + complemento_bono = garantizado_meta` sin solapamiento |
| `km_google` vs `km_didi` | ✅ Fuentes independientes — no hay doble contabilización |
| Variables primarias vs derivadas | ✅ Derivadas calculadas solo de primarias — sin circularidad |
| `franja_pico=1` vs `franja_pico=0` | ✅ Binario exhaustivo — toda jornada pertenece a una franja |
| `zona_arbitraje_optima=1` vs `alerta_critica=1` | ✅ Mutuamente excluyentes por construcción (1.73–1.84 ∩ ≥2.0 = ∅) |

### Exhaustividad Colectiva (Collectively Exhaustive)

| Dimensión | N Variables | Cobertura |
|-----------|-------------|-----------|
| Tiempo-Identificación | 5 | Toda la información temporal del turno |
| Distancia | 4 | Toda la información de kilómetros |
| Ingreso | 4 | Descomposición completa del ingreso bruto |
| Costo e Integridad | 2 | Gasto + bandera de integridad |
| Resultado | 4 | Toda la información de rentabilidad |
| Producción y Eficiencia | 7 | Toda la información de producción |
| Feature Engineering DSS | 3 | Todas las señales prescriptivas |
| **Total** | **28** | **Sin variables huérfanas** |

---

## NOTAS TÉCNICAS

**Moneda:** COP (Pesos Colombianos) · NO USD · NO EUR  
**Formato de tiempos:** Strings `HH:MM` — no decimales  
**Precisión numérica:** Financieras → INTEGER · Distancias → DECIMAL(8,2) · Ratios → DECIMAL(4,2)  
**Valores nulos:** 6 en `roi_diario` — documentados, no imputados  
**Outliers eliminados:** **0** — transparencia total

---

**Firmado:**  
*Diccionario de Variables MECE v1.2*  
*Actualizado: 2026-02-18 · Principio: Mutually Exclusive · Collectively Exhaustive*
