# 📊 Resultados del Análisis

## Estadísticas Descriptivas Globales

### Periodo de Análisis
- **Inicio:** 5 diciembre 2025
- **Fin:** 30 enero 2026
- **Días operativos:** 24
- **Días promedio/semana:** 3.0

### Métricas Agregadas

| Métrica | Valor |
|---------|-------|
| **KM Reales Pedaleados** | 1,526.3 km |
| **KM Reportados DiDi** | 2,513.3 km |
| **KM "Fantasma"** | 987.0 km (65% extra) |
| **Ratio Optimización Global** | **1.71x** |
| **Ingreso Total** | $4,279,030 COP |
| **Gastos Operativos** | $382,500 COP |
| **Desgaste Bicicleta** | $189,261 COP |
| **Utilidad Neta** | $4,009,530 COP |
| **Salario/Hora Promedio** | $35,784/h |

---

## Análisis 1: Distribución por Ratio de Optimización

### Clasificación de Días

| Nivel | Criterio | Días | % | RO Prom | Salario/H | Utilidad Prom |
|-------|----------|------|---|---------|-----------|---------------|
| 🚀 Excelente | RO ≥ 2.0x | 7 | 29% | 2.18x | $41,200 | $231,286 |
| 🟢 Bueno | 1.5 ≤ RO < 2.0 | 11 | 46% | 1.67x | $36,818 | $195,409 |
| 🟡 Neutro | 1.0 ≤ RO < 1.5 | 6 | 25% | 1.29x | $29,457 | $142,143 |
| 🔴 Malo | RO < 1.0 | 0 | 0% | - | - | - |

### Interpretación

✅ **Hallazgo Clave:** 72% de los días alcanzaron RO ≥ 1.5x

Esto demuestra que la estrategia de atajos urbanos es **consistentemente efectiva**, no un evento fortuito ocasional.

---

## Análisis 2: Impacto de Pedidos Cohete

### Clasificación por Eficiencia de Cohetes

| Nivel Cohetes | Días | Efic Prom | Utilidad | RO | Salario/H |
|---------------|------|-----------|----------|-----|-----------|
| **≥80% cohetes** | 15 | 93.5% | $198,520 | 1.72x | $39,215 |
| **60-79% cohetes** | 6 | 72.1% | $167,000 | 1.58x | $34,100 |
| **40-59% cohetes** | 2 | 53.5% | $152,500 | 1.51x | $31,850 |
| **<40% cohetes** | 2 | 28.6% | $121,000 | 1.42x | $26,200 |

### Correlación

```
Eficiencia Cohete ↑ → Utilidad ↑ (+64%)
Eficiencia Cohete ↑ → RO ↑ (+21%)
```

**Conclusión:** Estrategia de priorizar pedidos cohete es **económicamente óptima**

---

## Análisis 3: Top 10 Mejores Días

| Fecha | RO | Salario/H | Utilidad | Efic Cohetes | KM Reales |
|-------|-----|-----------|----------|--------------|-----------|
| 2025-12-25 | 1.67x | $52,340 | $282,256 | 57.1% | 86.5 |
| 2026-01-11 | 1.73x | $50,819 | $236,515 | 100.0% | 60.4 |
| 2025-12-21 | 1.43x | $44,891 | $234,754 | 100.0% | 94.8 |
| 2025-12-14 | 1.37x | $44,682 | $219,352 | 100.0% | 101.9 |
| 2025-12-20 | 1.44x | $44,177 | $234,351 | 90.0% | 102.0 |
| 2025-12-28 | 1.60x | $44,076 | $257,424 | 72.2% | 85.3 |
| 2026-01-18 | 1.99x | $43,947 | $180,048 | 89.5% | 44.0 |
| 2025-12-07 | 1.83x | $43,409 | $205,483 | 82.4% | 66.8 |
| 2025-12-06 | 1.66x | $40,194 | $162,008 | 100.0% | 72.6 |
| 2026-01-01 | 1.67x | $39,817 | $175,884 | 70.6% | 57.9 |

### Patrón Identificado

**Mejor día (2025-12-25):**
- Combina **alto volumen** (21 pedidos)
- Con **alta eficiencia** (57% cohetes)
- Y **duración extendida** (10.7 horas)

**No es solo sobre RO:** El mejor salario/hora resulta de balancear:
1. RO moderado-alto (1.5-2.0x)
2. Volumen sustancial (15-20 pedidos)
3. Duración óptima (8-11 horas)

---

## Análisis 4: Peores 5 Días

| Fecha | RO | Salario/H | Utilidad | Razón Probable |
|-------|-----|-----------|----------|----------------|
| 2026-01-08 | 1.59x | $9,657 | $27,316 | Bajo volumen (3 ped) |
| 2026-01-24 | 1.55x | $10,894 | $25,133 | Bajo volumen (6 ped) + gasto alto |
| 2025-12-13 | 1.46x | $15,642 | $77,175 | Gasto operativo excepcional ($58k) |
| 2026-01-12 | 1.43x | $20,551 | $79,624 | Turno corto (6.8h) |
| 2026-01-17 | 1.72x | $29,760 | $99,160 | Bajo volumen (11 ped) |

### Insight

**Factores de bajo rendimiento:**
1. ❌ Volumen bajo (<8 pedidos)
2. ❌ Gastos excepcionales (>$30k)
3. ❌ Turnos muy cortos (<5 horas)

---

## Análisis 5: KM Reales vs Reportados (Detalle)

### Top 5 Mayor Diferencia Absoluta

| Fecha | KM Reales | KM DiDi | Diferencia | RO | Ventaja % |
|-------|-----------|---------|------------|-----|-----------|
| 2025-12-08 | 104.61 | 135.40 | +30.79 | 1.29x | +29% |
| 2025-12-06 | 72.58 | 120.70 | +48.12 | 1.66x | +66% |
| 2025-12-07 | 66.79 | 122.50 | +55.71 | 1.83x | +83% |
| 2025-12-25 | 86.50 | 144.70 | +58.20 | 1.67x | +67% |
| 2025-12-20 | 102.02 | 146.80 | +44.78 | 1.44x | +44% |

### Top 5 Mayor RO Relativo

| Fecha | KM Reales | KM DiDi | RO | Ventaja % |
|-------|-----------|---------|-----|-----------|
| 2026-01-18 | 43.98 | 87.50 | **1.99x** | +99% |
| 2025-12-05 | 45.06 | 88.60 | 1.97x | +97% |
| 2025-12-07 | 66.79 | 122.50 | 1.83x | +83% |
| 2026-01-11 | 60.38 | 104.70 | 1.73x | +73% |
| 2026-01-17 | 30.96 | 53.30 | 1.72x | +72% |

**Insight:** Días con 40-60 km reales tienden a tener **mayor RO** que días con >100 km, sugiriendo que en distancias medias hay más oportunidad de atajos.

---

## Análisis 6: Eficiencia Temporal

### Velocidad Operativa

| Rango km/h | Días | Salario/H Prom | Utilidad Prom |
|------------|------|----------------|---------------|
| ≥10 km/h | 8 | $42,150 | $215,000 |
| 8-10 km/h | 11 | $36,800 | $185,000 |
| <8 km/h | 6 | $28,900 | $142,000 |

**Correlación:** Mayor velocidad operativa → Mayor salario/hora

### Velocidad de Enganche

| Min/Pedido | Días | Eficiencia | Observación |
|------------|------|------------|-------------|
| <30 min | 6 | Alta | Turnos muy productivos |
| 30-40 min | 13 | Media | Rango típico |
| >40 min | 6 | Baja | Días con mucha espera |

---

## Análisis 7: Tendencia Temporal

### Por Mes

| Mes | Días | RO Prom | Salario/H | Utilidad Total |
|-----|------|---------|-----------|----------------|
| 2025-12 | 13 | 1.59x | $37,215 | $2,123,000 |
| 2026-01 | 12 | 1.72x | $34,120 | $1,584,269 |

**Observación:** 
- RO mejoró +8% en enero
- Pero salario/hora bajó -8%
- Razón: Menor volumen de pedidos en enero

### Por Semana

| Semana | Días | RO | Utilidad | Tendencia |
|--------|------|----|----------|-----------|
| Sem 49 | 4 | 1.63x | $733,000 | ↗️ |
| Sem 50 | 2 | 1.42x | $388,000 | ↘️ |
| Sem 51 | 4 | 1.56x | $890,000 | ↗️ |
| Sem 52 | 3 | 1.58x | $535,000 | → |
| Sem 1 | 5 | 1.69x | $740,269 | ↗️ |
| Sem 2 | 2 | 1.67x | $223,000 | → |
| Sem 3 | 3 | 1.76x | $303,000 | ↗️ |
| Sem 4 | 2 | 1.53x | $195,000 | ↘️ |

**Sin tendencia clara:** RO se mantiene estable alrededor de 1.6-1.7x

---

## Análisis 8: ROI y Rentabilidad

### Desglose de Costos

| Concepto | Monto | % del Ingreso |
|----------|-------|---------------|
| **Ingreso Bruto** | $4,279,030 | 100% |
| Gastos Operativos | -$382,500 | 8.9% |
| Desgaste Bici | -$0 | 0% |
| **Utilidad Neta** | **$4,009,530** | **93.7%** |

### ROI

```
ROI = (Utilidad / Costos) × 100
ROI = ($4,009,530 / $161,779) × 100
ROI = 2,479%
```

**Cada peso invertido genera $24.79 de utilidad**

### Comparación con Salario Mínimo

| Métrica | Valor |
|---------|-------|
| Salario mínimo 2026 (COP) | $6,667/hora |
| Salario efectivo promedio | $35,784/hora |
| **Múltiplo sobre mínimo** | **5.37x** |

---

## Análisis 9: Correlaciones Estadísticas

### Matriz de Correlación (Pearson)

| | RO | Utilidad | Salario/H | Efic Cohete |
|-|-----|----------|-----------|-------------|
| **RO** | 1.00 | 0.32 | 0.41 | 0.28 |
| **Utilidad** | 0.32 | 1.00 | 0.89 | 0.51 |
| **Salario/H** | 0.41 | 0.89 | 1.00 | 0.47 |
| **Efic Cohete** | 0.28 | 0.51 | 0.47 | 1.00 |

### Interpretación

1. **RO ↔ Salario/H:** Correlación moderada (r=0.41)
   - Mayor RO **SÍ** mejora salario, pero no es el único factor

2. **Utilidad ↔ Salario/H:** Correlación fuerte (r=0.89)
   - Como esperado: más utilidad = más salario/hora

3. **Eficiencia Cohete ↔ Utilidad:** Correlación moderada (r=0.51)
   - Más cohetes **SÍ** mejora utilidad significativamente

---

## Análisis 10: Rangos Óptimos

### KM Reales Óptimo

| Rango KM | Días | RO Prom | Salario/H | Velocidad |
|----------|------|---------|-----------|-----------|
| <40 km | 5 | 1.68x | $30,200 | 8.1 km/h |
| 40-60 km | 8 | **1.74x** | $38,500 | 9.2 km/h |
| 60-80 km | 7 | 1.62x | $39,100 | 8.8 km/h |
| ≥80 km | 5 | 1.56x | $41,800 | 9.5 km/h |

**Óptimo:** 40-60 km reales maximiza RO

### Pedidos Óptimo

| Total Pedidos | Días | Utilidad Prom | Salario/H |
|---------------|------|---------------|-----------|
| <10 | 4 | $98,000 | $23,100 |
| 10-15 | 10 | $163,000 | $35,400 |
| 15-20 | 9 | $221,000 | $41,200 |
| ≥20 | 2 | $282,000 | $48,600 |

**Óptimo:** 15-20 pedidos por día

---

## Conclusiones

### Hallazgos Principales

1. ✅ **RO Global 1.71x:** Ventaja competitiva cuantificable y consistente
2. ✅ **Estrategia Cohetes:** +39% utilidad con alta eficiencia de cohetes
3. ✅ **ROI 648%:** Modelo de negocio altamente rentable
4. ✅ **Salario 5.37x mínimo:** Ingreso significativamente superior al mínimo legal

### Recomendaciones Operativas

1. 📈 **Priorizar pedidos cohete** cuando RO > 1.5x
2. 📍 **Operar en zonas con infraestructura ciclística** (Kennedy/Fontibón)
3. ⏱️ **Turnos de 8-11 horas** con 15-20 pedidos
4. 💰 **Controlar gastos operativos** bajo $25k/día

### Limitaciones

- Muestra N=1 (un operador)
- Periodo corto (2 meses)
- Zona específica (Kennedy/Fontibón)
- Sin control de variables externas

---

**Documento de Resultados v1.0**  
**Fecha:** Febrero 2026  
**Autor:** Iván Felipe Castro Pinzón
