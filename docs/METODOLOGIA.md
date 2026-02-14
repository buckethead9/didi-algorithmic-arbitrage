# METODOLOGÍA
## Protocolo de Auditoría de Arbitraje Algorítmico

**Proyecto:** Análisis de Asimetría Topológica DiDi Food vs Google Maps  
**Versión:** 1.0.0  
**Periodo:** 2025-12-05 a 2026-01-31 (26 días operativos)  
**Principio:** Transparencia Radical - La Verdad por encima de la Armonía

---

## 1. OBJETIVO DEL ESTUDIO

Cuantificar y analizar la **asimetría algorítmica** entre las rutas calculadas por DiDi App (optimizadas para motocicletas) y Google Maps (ciclorrutas), con el fin de:

1. Identificar oportunidades de arbitraje operativo
2. Validar la rentabilidad del modelo de negocio
3. Detectar patrones de optimización de rutas
4. Documentar anomalías técnicas y operativas

---

## 2. DISEÑO DEL ESTUDIO

### 2.1 Tipo de Estudio
**Observacional, longitudinal, descriptivo**  
- Sin intervención experimental
- Registro natural de operaciones
- 26 días no consecutivos

### 2.2 Unidad de Análisis
**Día Operativo:** Turno completo desde activación hasta desactivación en DiDi App, independientemente de si cruza la medianoche.

### 2.3 Población
**Operador único:** Repartidor de DiDi Food en Bogotá, Colombia  
**Vehículo:** Motocicleta (no bicicleta)  
**Zona:** Bogotá D.C., operación urbana

---

## 3. PROTOCOLO DE RECOLECCIÓN DE DATOS

### 3.1 Fuentes de Datos Primarias

#### 3.1.1 DiDi App (Automática)
- `h_inicio`: Timestamp de activación
- `h_fin`: Timestamp de desactivación
- `garantizado_meta`: Ingreso total garantizado
- `ingreso_base`: Ingreso base por pedidos
- `complemento_bono`: Bono por cumplir meta
- `unidades_progreso`: Unidades contabilizadas por DiDi

#### 3.1.2 Google Maps API (Manual)
- `km_google`: Distancia total en modo "bicicleta"
- Cálculo post-turno para cada destino del día

#### 3.1.3 Registro Manual del Operador
- `fecha`: Fecha del turno
- `km_didi`: Distancia mostrada en DiDi App
- `pedidos_fisicos`: Conteo real de entregas
- `gastos_operativos`: Gastos del día (combustible, mantenimiento)

### 3.2 Protocolo de Captura

**Momento 1: Pre-Turno**
- Registrar fecha y hora de inicio

**Momento 2: Durante el Turno**
- Contar pedidos físicos completados
- Registrar gastos en tiempo real

**Momento 3: Post-Turno**
- Capturar `km_didi` de DiDi App
- Calcular `km_google` con Google Maps API
- Registrar hora de fin y métricas finales

### 3.3 Filtro Cognitivo del Operador

**Definición:** Proceso mental mediante el cual el operador decide qué pedidos aceptar o rechazar.

**Variables de decisión:**
1. Distancia del pedido
2. Ubicación del restaurante
3. Zona de entrega (seguridad)
4. Tráfico esperado
5. Meta de unidades pendientes

**Impacto en los datos:**
- Los pedidos rechazados **no** están en el dataset
- Solo se registran pedidos aceptados y completados
- Sesgo de selección positivo hacia pedidos rentables

**Implicación metodológica:**  
Los datos reflejan la **operación optimizada** del repartidor, no una muestra aleatoria de todos los pedidos disponibles.

---

## 4. TRATAMIENTO DE CASOS ESPECIALES

### 4.1 Turnos con Cruce de Medianoche

**Definición:** Turno que comienza en un día calendario y termina en el siguiente.

**Ejemplo:**
- Inicio: `2025-12-13 17:01`
- Fin: `2025-12-14 0:12`

**Problema Técnico:**  
Si se calcula `h_fin - h_inicio` sin ajuste:  
`0:12 - 17:01 = -16:49` (resultado negativo)

**Solución: Día Operativo**  
El "Día Operativo" es una unidad **indivisible**. Si `h_fin < h_inicio`, se suma 24 horas a `h_fin`:

```python
def calcular_duracion_turno(h_inicio, h_fin):
    minutos_inicio = h_inicio.hora * 60 + h_inicio.minutos
    minutos_fin = h_fin.hora * 60 + h_fin.minutos
    
    # Detectar cruce de medianoche
    if minutos_fin < minutos_inicio:
        minutos_fin += 1440  # +24 horas
    
    duracion_minutos = minutos_fin - minutos_inicio
    return duracion_minutos / 60.0
```

**Resultado:**  
`17:01 a 0:12` → `7.18 horas` (no `6.18`)

**Casos en el dataset:** 4 turnos con cruce de medianoche

**Implicación:**  
- No fragmentar turnos en dos días separados
- Asignar el turno a la fecha de inicio (`fecha`)
- La duración refleja el tiempo real trabajado

### 4.2 Días con Gasto $0

**Observación:** 6 días registran `gastos_operativos = 0`

**Posibles causas:**
1. Omisión de registro manual
2. Uso de moto compartida (sin gasto personal de combustible)
3. Días de prueba/cortesía con DiDi

**Tratamiento:**
- **ROI Diario:** No calculable (`NaN`)
- **Utilidad Neta:** Se registra normalmente
- **Documentación:** Clasificados como anomalías técnicas

**Impacto en métricas globales:**
- ROI Global se calcula sobre **total de gastos** ($431,000 COP)
- Los días con gasto $0 **sí** se incluyen en el numerador (ingresos)
- Esto infla artificialmente el ROI, pero refleja la realidad operativa

**Decisión de auditoría:**  
Reportar la anomalía, **no** excluir los registros del dataset.

### 4.3 Eficiencia de Cumplimiento < 1.0

**Definición:**  
`eficiencia_cumplimiento = unidades_progreso / pedidos_fisicos`

**Caso común:**  
`pedidos_fisicos = 12`, `unidades_progreso = 11` → `eficiencia = 0.92`

**Interpretación:**
- DiDi no contabilizó 1 pedido para la meta
- Posible pedido cancelado después de recoger
- Pedido fuera de zona de meta

**Tratamiento:**  
No ajustamos los datos. Los pedidos físicos son la **fuente de verdad** para el operador, las unidades de progreso son la **fuente de verdad** para DiDi.

---

## 5. DEFINICIÓN DE ASIMETRÍA TOPOLÓGICA

### 5.1 Concepto Teórico

**Asimetría Topológica:** Discrepancia sistemática entre la distancia calculada por dos algoritmos de routing para el mismo conjunto de destinos.

**Hipótesis:**  
DiDi App calcula rutas más largas que Google Maps porque:
1. **Optimiza para motocicletas** (no bicicletas ni peatones)
2. **Considera tráfico en tiempo real** (rutas menos directas pero más rápidas)
3. **Evita ciclorrutas** que no son aptas para motos

### 5.2 Métrica: Ratio de Optimización (RO)

**Fórmula:**
```
RO = km_didi / km_google
```

**Interpretación:**
- `RO = 1.0` → Ambas apps calculan la misma distancia
- `RO > 1.0` → DiDi calcula rutas más largas
- `RO < 1.0` → DiDi calcula rutas más cortas (inusual)

**Valor empírico:**
```
RO Global = 2,601.89 km / 1,571.38 km = 1.66x
```

**Conclusión:**  
En promedio, las rutas de DiDi son **66% más largas** que las de Google Maps.

### 5.3 Implicaciones Operativas

**Ventaja del operador:**
- DiDi paga por `garantizado_meta` (fijo), no por km recorridos
- El operador puede elegir rutas más cortas (ciclorrutas) y ahorrar tiempo/combustible
- Arbitraje: Cobrar por rutas largas, ejecutar rutas cortas

**Riesgo:**
- Si DiDi detecta desviaciones consistentes, puede ajustar el algoritmo o penalizar
- Ética: ¿Es legítimo tomar rutas más cortas si DiDi espera rutas más largas?

**Respuesta del estudio:**  
El operador **no está hackeando el sistema**. DiDi calcula rutas para motos en tráfico, el operador ejecuta rutas de bicicleta. Es una ineficiencia del algoritmo de DiDi, no una trampa del operador.

---

## 6. LIMPIEZA Y TRANSFORMACIÓN DE DATOS

### 6.1 Normalización de Kilómetros

**Problema:** CSV tiene formato `"45,06 km"` (coma decimal + sufijo)

**Solución:**
```python
def limpiar_kilometros(valor_km):
    # "45,06 km" → "45.06" → 45.06
    valor_str = str(valor_km).replace(" km", "").replace(",", ".")
    return float(valor_str)
```

### 6.2 Cálculo de Métricas Derivadas

Ver `DICCIONARIO_VARIABLES.md` para fórmulas completas de las 13 variables derivadas.

### 6.3 Validación de Integridad

**Reglas de validación:**
1. `duracion_horas > 0` para todos los registros
2. `km_didi >= km_google` en la mayoría de los casos (salvo excepciones)
3. `utilidad_neta = garantizado_meta - gastos_operativos`
4. `garantizado_meta = ingreso_base + complemento_bono`

**Registros inválidos:** 0 (100% de integridad)

---

## 7. MÉTRICAS GLOBALES DE AUDITORÍA

### 7.1 Valores Auditados (Transparencia Radical)

| Métrica | Valor | Unidad |
|---------|-------|--------|
| **N (Registros)** | 26 | días |
| **Total Ingresos** | $4,440,530 | COP |
| **Total Gastos** | $431,000 | COP |
| **Utilidad Neta** | $4,009,530 | COP |
| **ROI Global** | 930.28 | % |
| **RO Global** | 1.66 | x |
| **Múltiplo de Ingreso** | 10.30 | x |
| **Total Pedidos** | 363 | pedidos |
| **Duración Total** | 236.72 | horas |

### 7.2 Diferenciación Semántica

**NO confundir:**

- **RO (Ratio de Optimización):** `km_didi / km_google = 1.66x`  
  Mide eficiencia de distancia física

- **Múltiplo de Ingreso:** `Ingresos / Gastos = 10.30x`  
  Mide relación financiera

**Ambas métricas son multiplicadores, pero NO son la misma cosa.**

---

## 8. LIMITACIONES DEL ESTUDIO

### 8.1 Sesgo de Selección
- Solo se registran pedidos aceptados y completados
- Pedidos rechazados no están en el dataset

### 8.2 Operador Único
- Los resultados no son generalizables a todos los repartidores
- Experiencia y estrategia del operador afectan las métricas

### 8.3 Periodo Limitado
- 26 días no consecutivos no capturan estacionalidad completa
- Falta análisis de fines de semana vs días laborales

### 8.4 Zona Geográfica
- Resultados específicos de Bogotá
- Topografía, tráfico y regulaciones locales afectan las rutas

### 8.5 Días con Gasto $0
- 6 días sin gastos registrados generan anomalías en ROI diario
- ROI global puede estar artificialmente inflado

---

## 9. CONSIDERACIONES ÉTICAS

### 9.1 Transparencia con DiDi
Este análisis **no** implica evasión de políticas de DiDi. El operador:
- Cumple todas las entregas
- No falsifica ubicaciones
- Sigue rutas legales y seguras

### 9.2 Privacidad
- No se revelan datos personales del operador
- No se exponen direcciones de clientes
- Solo métricas agregadas

### 9.3 Uso de Datos
- Los datos son propiedad del operador (registros personales)
- DiDi App solo proporciona métricas agregadas, no trazas GPS

---

## 10. CONCLUSIÓN METODOLÓGICA

Este estudio demuestra que:

1. **Es posible cuantificar la asimetría algorítmica** entre DiDi y Google Maps
2. **El tratamiento de medianoche es crítico** para cálculos precisos
3. **El arbitraje operativo es real:** Rutas de DiDi son 66% más largas
4. **La rentabilidad es excepcional:** ROI de 930.28%
5. **Las anomalías deben documentarse**, no ocultarse

**Principio final:**  
> "Un análisis honesto con limitaciones documentadas es más valioso que un análisis perfecto con datos maquillados."

---

**Firmado:**  IVÁN FELIPE CASTRO PINZÓN
*Pipeline de Auditoría de Integridad v1.0*  
*Fecha: 2026-02-13*  
*Principio: La Verdad por encima de la Armonía*
