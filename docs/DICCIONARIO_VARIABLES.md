# DICCIONARIO DE VARIABLES
## Pipeline de Auditoría - Arbitraje Algorítmico DiDi Food

**Versión:** 1.0.0  
**Dataset:** didi_analisis_12_01.csv  
**N:** 26 registros  
**Periodo:** 2025-12-05 a 2026-01-31

---

## PRINCIPIO DE INMUTABILIDAD

> Una vez definida una variable en este diccionario, debe usarse con el mismo nombre y fórmula en los otros 4 documentos (main.py, README.md, METODOLOGIA.md, RESULTADOS.md, ANALISIS_SQL_FINAL.sql).

---

## VARIABLES PRIMARIAS (9)

### 1. `fecha`
**Tipo:** DATE  
**Descripción:** Fecha del día operativo en formato ISO 8601  
**Formato:** YYYY-MM-DD  
**Ejemplo:** `2025-12-05`  
**Fuente:** Registro manual del operador

---

### 2. `h_inicio`
**Tipo:** TIME  
**Descripción:** Hora de inicio del turno  
**Formato:** HH:MM (24 horas)  
**Ejemplo:** `17:05`  
**Fuente:** Timestamp de activación en DiDi App  
**Nota:** Puede ser en la mañana, tarde o noche

---

### 3. `h_fin`
**Tipo:** TIME  
**Descripción:** Hora de finalización del turno  
**Formato:** HH:MM (24 horas)  
**Ejemplo:** `23:23` o `0:12` (si cruza medianoche)  
**Fuente:** Timestamp de desactivación en DiDi App  
**Crítico:** Si `h_fin < h_inicio`, el turno cruzó la medianoche

---

### 4. `km_google`
**Tipo:** DECIMAL(8,2)  
**Descripción:** Distancia total recorrida según Google Maps (ciclorrutas)  
**Unidad:** Kilómetros (km)  
**Ejemplo:** `45.06`  
**Fuente:** Google Maps API con modo "bicicleta"  
**Limpieza:** `"45,06 km"` → `45.06`

---

### 5. `km_didi`
**Tipo:** DECIMAL(8,2)  
**Descripción:** Distancia total recorrida según DiDi App (rutas motorizadas)  
**Unidad:** Kilómetros (km)  
**Ejemplo:** `88.6`  
**Fuente:** DiDi App (cálculo interno de la plataforma)  
**Limpieza:** `"88,6 km"` → `88.6`

---

### 6. `garantizado_meta`
**Tipo:** INTEGER  
**Descripción:** Ingreso total garantizado por DiDi al cumplir la meta del turno  
**Unidad:** Pesos Colombianos (COP)  
**Ejemplo:** `130000`  
**Fórmula:** `ingreso_base + complemento_bono`  
**Fuente:** Plataforma DiDi

---

### 7. `ingreso_base`
**Tipo:** INTEGER  
**Descripción:** Ingreso base por pedidos completados (sin bonos)  
**Unidad:** COP  
**Ejemplo:** `66676`  
**Fuente:** Plataforma DiDi

---

### 8. `complemento_bono`
**Tipo:** INTEGER  
**Descripción:** Bono adicional al cumplir la meta de pedidos  
**Unidad:** COP  
**Ejemplo:** `63324`  
**Fuente:** Plataforma DiDi  
**Fórmula:** `garantizado_meta - ingreso_base`

---

### 9. `pedidos_fisicos`
**Tipo:** INTEGER  
**Descripción:** Número de pedidos completados y entregados  
**Unidad:** Pedidos  
**Ejemplo:** `12`  
**Fuente:** Conteo manual del operador  
**Nota:** Incluye pedidos cancelados después de recoger

---

### 10. `unidades_progreso`
**Tipo:** INTEGER  
**Descripción:** Unidades de progreso contabilizadas por DiDi para cumplir la meta  
**Unidad:** Unidades  
**Ejemplo:** `11`  
**Fuente:** DiDi App  
**Nota:** Puede ser menor que `pedidos_fisicos` si DiDi no contabilizó algunos pedidos

---

### 11. `gastos_operativos`
**Tipo:** INTEGER  
**Descripción:** Gastos totales del turno (combustible, mantenimiento, alquiler de moto, etc.)  
**Unidad:** COP  
**Ejemplo:** `17000`  
**Fuente:** Registro manual del operador  
**Crítico:** Algunos días tienen `$0` (anomalía técnica)

---

## VARIABLES DERIVADAS (13)

### 12. `duracion_horas`
**Tipo:** DECIMAL(5,2)  
**Descripción:** Duración total del turno en horas  
**Unidad:** Horas  
**Fórmula:**  
```python
def calcular_duracion_turno(h_inicio, h_fin):
    minutos_inicio = h_inicio.hora * 60 + h_inicio.minutos
    minutos_fin = h_fin.hora * 60 + h_fin.minutos
    
    # Tratamiento de medianoche
    if minutos_fin < minutos_inicio:
        minutos_fin += 1440  # +24 horas
    
    duracion_minutos = minutos_fin - minutos_inicio
    return duracion_minutos / 60.0
```
**Ejemplo:** `17:01 a 0:12` → `7.18 horas` (no `6.18`)  
**Crítico:** El "Día Operativo" es una unidad, sin fragmentar turnos

---

### 13. `utilidad_neta`
**Tipo:** INTEGER  
**Descripción:** Ganancia neta después de gastos  
**Unidad:** COP  
**Fórmula:**  
```python
utilidad_neta = garantizado_meta - gastos_operativos
```
**Ejemplo:** `130000 - 17000 = 113000`

---

### 14. `km_por_pedido_google`
**Tipo:** DECIMAL(5,2)  
**Descripción:** Distancia promedio por pedido según Google Maps  
**Unidad:** km/pedido  
**Fórmula:**  
```python
km_por_pedido_google = km_google / pedidos_fisicos
```
**Ejemplo:** `45.06 / 12 = 3.76 km/pedido`

---

### 15. `km_por_pedido_didi`
**Tipo:** DECIMAL(5,2)  
**Descripción:** Distancia promedio por pedido según DiDi App  
**Unidad:** km/pedido  
**Fórmula:**  
```python
km_por_pedido_didi = km_didi / pedidos_fisicos
```
**Ejemplo:** `88.6 / 12 = 7.38 km/pedido`

---

### 16. `ratio_optimizacion` (RO)
**Tipo:** DECIMAL(4,2)  
**Descripción:** Ratio de eficiencia de distancia (asimetría algorítmica)  
**Unidad:** Factor multiplicador (x)  
**Fórmula:**  
```python
ratio_optimizacion = km_didi / km_google
```
**Ejemplo:** `88.6 / 45.06 = 1.97x`  
**Interpretación:** DiDi calcula rutas 97% más largas que Google Maps  
**Uso exclusivo:** Eficiencia de distancia física  
**NO confundir con:** Múltiplo de Ingreso (variable financiera)

---

### 17. `ingreso_por_km_google`
**Tipo:** DECIMAL(8,2)  
**Descripción:** Ingreso por kilómetro recorrido según Google Maps  
**Unidad:** COP/km  
**Fórmula:**  
```python
ingreso_por_km_google = garantizado_meta / km_google
```
**Ejemplo:** `130000 / 45.06 = 2885.04 COP/km`

---

### 18. `ingreso_por_km_didi`
**Tipo:** DECIMAL(8,2)  
**Descripción:** Ingreso por kilómetro recorrido según DiDi App  
**Unidad:** COP/km  
**Fórmula:**  
```python
ingreso_por_km_didi = garantizado_meta / km_didi
```
**Ejemplo:** `130000 / 88.6 = 1467.27 COP/km`

---

### 19. `ingreso_por_hora`
**Tipo:** DECIMAL(8,2)  
**Descripción:** Ingreso promedio por hora trabajada  
**Unidad:** COP/hora  
**Fórmula:**  
```python
ingreso_por_hora = garantizado_meta / duracion_horas
```
**Ejemplo:** `130000 / 6.3 = 20634.92 COP/hora`

---

### 20. `utilidad_por_hora`
**Tipo:** DECIMAL(8,2)  
**Descripción:** Utilidad neta promedio por hora trabajada  
**Unidad:** COP/hora  
**Fórmula:**  
```python
utilidad_por_hora = utilidad_neta / duracion_horas
```
**Ejemplo:** `113000 / 6.3 = 17936.51 COP/hora`

---

### 21. `eficiencia_cumplimiento`
**Tipo:** DECIMAL(4,2)  
**Descripción:** Proporción de pedidos contabilizados por DiDi vs pedidos físicos  
**Unidad:** Factor (0 a 1)  
**Fórmula:**  
```python
eficiencia_cumplimiento = unidades_progreso / pedidos_fisicos
```
**Ejemplo:** `11 / 12 = 0.92`  
**Interpretación:**  
- `1.0` = DiDi contabilizó todos los pedidos
- `< 1.0` = Algunos pedidos no fueron contabilizados
- `> 1.0` = DiDi contabilizó más unidades (bonos especiales)

---

### 22. `proporcion_bono`
**Tipo:** DECIMAL(4,2)  
**Descripción:** Proporción del ingreso que proviene de bonos  
**Unidad:** Factor (0 a 1)  
**Fórmula:**  
```python
proporcion_bono = complemento_bono / garantizado_meta
```
**Ejemplo:** `63324 / 130000 = 0.49` (49%)

---

### 23. `roi_diario`
**Tipo:** DECIMAL(8,2)  
**Descripción:** Retorno de Inversión del día  
**Unidad:** Porcentaje (%)  
**Fórmula:**  
```python
if gastos_operativos > 0:
    roi_diario = (utilidad_neta / gastos_operativos) * 100
else:
    roi_diario = NaN  # No calculable
```
**Ejemplo:** `(113000 / 17000) * 100 = 664.71%`  
**Crítico:** Solo calculable si `gastos_operativos > 0`

---

### 24. `rentabilidad_binaria`
**Tipo:** BOOLEAN (0 o 1)  
**Descripción:** Indicador de éxito financiero del día  
**Fórmula:**  
```python
rentabilidad_binaria = 1 if utilidad_neta > 0 else 0
```
**Interpretación:**  
- `1` = Día rentable
- `0` = Día con pérdidas

---

## MÉTRICAS GLOBALES (AGREGADAS)

### `total_ingresos`
**Fórmula:** `SUM(garantizado_meta)`  
**Valor Auditado:** `$4,440,530 COP`

### `total_gastos`
**Fórmula:** `SUM(gastos_operativos)`  
**Valor Auditado:** `$431,000 COP`

### `utilidad_neta_global`
**Fórmula:** `total_ingresos - total_gastos`  
**Valor:** `$4,009,530 COP`

### `roi_global`
**Fórmula:** `(utilidad_neta_global / total_gastos) * 100`  
**Valor:** `930.28%`

### `ro_global`
**Fórmula:** `SUM(km_didi) / SUM(km_google)`  
**Valor:** `1.66x`  
**Interpretación:** En promedio, DiDi calcula rutas 66% más largas

### `multiplo_ingreso`
**Fórmula:** `total_ingresos / total_gastos`  
**Valor:** `10.30x`  
**Interpretación:** Cada peso invertido genera $10.30 COP de ingresos

---

## DIFERENCIACIÓN SEMÁNTICA DE RATIOS

### ⚠️ ADVERTENCIA CRÍTICA

**NO confundir estas dos métricas:**

| Métrica | Uso | Fórmula | Valor |
|---------|-----|---------|-------|
| **RO (Ratio de Optimización)** | Eficiencia de distancia física | `km_didi / km_google` | **1.66x** |
| **Múltiplo de Ingreso** | Relación financiera | `Ingresos / Gastos` | **10.30x** |

**RO** mide cuánto más larga es la ruta de DiDi vs Google Maps.  
**Múltiplo de Ingreso** mide cuántos pesos generas por cada peso invertido.

---

## ANOMALÍAS DOCUMENTADAS

1. **Días con Gasto $0:** 6 registros (ROI no calculable en esos días)
2. **Turnos con cruce de medianoche:** 4 registros (requieren tratamiento especial)
3. **Eficiencia de cumplimiento < 1.0:** DiDi no contabilizó algunos pedidos

---

## NOTAS TÉCNICAS

- **Precisión:** Todas las métricas usan 2 decimales
- **Moneda:** COP (Pesos Colombianos), **NO USD**
- **Tratamiento de NULL:** Si `pedidos_fisicos = 0`, las métricas por pedido retornan `0` (no error)
- **Codificación:** UTF-8

---

**Última Actualización:** 2026-02-13  
**Firmado:** Pipeline de Auditoría de Integridad v1.0
