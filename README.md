# Pipeline de Auditoría - Arbitraje Algorítmico DiDi Food

```
╔════════════════════════════════════════════════════════════════╗
║                    REGISTRO INMUTABLE                          ║
║           Arquitectura de Transparencia Radical                ║
╚════════════════════════════════════════════════════════════════╝
```

**Versión:** 1.0.0  
**Autor:** Iván Felipe Castro Pinzón 
**Fecha:** 2026-02-13  
**Principio:** La Verdad por encima de la Armonía

---

## 📋 TABLA DE CONTENIDOS

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Pipeline de Tres Capas](#pipeline-de-tres-capas)
4. [Estructura del Repositorio](#estructura-del-repositorio)
5. [Instalación y Uso](#instalación-y-uso)
6. [Resultados Clave](#resultados-clave)
7. [Documentación Técnica](#documentación-técnica)
8. [Consideraciones Éticas](#consideraciones-éticas)
9. [Licencia y Atribuciones](#licencia-y-atribuciones)

---

## 🎯 RESUMEN EJECUTIVO

### ¿Qué es este proyecto?

Este repositorio contiene un **pipeline de auditoría de integridad** para analizar la **asimetría algorítmica** entre las rutas calculadas por DiDi App (para motocicletas) y Google Maps (ciclorrutas). El objetivo es cuantificar oportunidades de arbitraje operativo y validar la rentabilidad del modelo de negocio.

### Resultados Clave (N=26 días)

```
💰 Ingresos Totales:        $4,440,530 COP
💸 Gastos Totales:          $431,000 COP
💵 Utilidad Neta:           $4,009,530 COP
📈 ROI Global:              930.28%
🔢 Múltiplo de Ingreso:     10.30x
🛣️  RO Global (Asimetría):  1.66x
```

**Conclusión:** DiDi calcula rutas **66% más largas** que Google Maps, pero el modelo sigue siendo altamente rentable con un ROI de **930.28%**.

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Concepto: Exoesqueleto Mental

Este proyecto es un **exoesqueleto mental** para la toma de decisiones basada en datos. No es solo un script de análisis, es una **estructura de pensamiento** que garantiza:

1. **Integridad de datos:** Sin maquillaje ni eufemismos.
2. **Trazabilidad:** Cada métrica tiene una fórmula explícita.
3. **Inmutabilidad:** Las definiciones son consistentes en todos los documentos.
4. **Transparencia radical:** Las anomalías se documentan, no se ocultan.

### Filosofía de Diseño

> "Un análisis honesto con limitaciones documentadas es más valioso que un análisis perfecto con datos maquillados."

- **NO** redondear métricas para que "se vean mejor"
- **NO** excluir outliers sin justificación
- **NO** usar moneda incorrecta (COP, no USD)
- **SÍ** documentar fallas técnicas (días con gasto $0)
- **SÍ** reportar ROI real (930.28%, no 1,000%)

---

## 🔄 PIPELINE DE TRES CAPAS

```
┌─────────────────────────────────────────────────────────────┐
│                     CAPA 1: INGESTA                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────────┐   │
│  │ CSV Raw  │──▶│ main.py  │──▶│ CSV Procesado        │   │
│  │ (Sucio)  │   │ (Python) │   │ (Limpio + Derivadas) │   │
│  └──────────┘   └──────────┘   └──────────────────────┘   │
│                                                             │
│  • Limpieza de kilómetros: "45,06 km" → 45.06             │
│  • Tratamiento de medianoche: 17:01-0:12 → 7.18 horas     │
│  • Cálculo de 13 variables derivadas                       │
│  • Validación de integridad                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   CAPA 2: AUDITORÍA                         │
│  ┌──────────────┐   ┌───────────┐   ┌───────────────────┐ │
│  │ CSV Procesado│──▶│ MySQL 8.0 │──▶│ Vistas de Análisis│ │
│  │              │   │ (opcional)│   │ (10 tablas)       │ │
│  └──────────────┘   └───────────┘   └───────────────────┘ │
│                                                             │
│  • Carga a base de datos (opcional)                        │
│  • 10 vistas SQL de análisis                               │
│  • Identificación de anomalías                             │
│  • Cálculo de métricas globales auditadas                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                 CAPA 3: VISUALIZACIÓN                       │
│  ┌──────────────┐   ┌────────────┐   ┌─────────────────┐  │
│  │ RESULTADOS.md│   │ Dashboards │   │ BI Tools        │  │
│  │ (10 tablas)  │   │ (futuros)  │   │ (Power BI, etc.)│  │
│  └──────────────┘   └────────────┘   └─────────────────┘  │
│                                                             │
│  • Tablas de análisis en Markdown                          │
│  • Dashboard ejecutivo                                     │
│  • Gráficos de dispersión (futuro)                         │
│  • Integración con BI (opcional)                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 ESTRUCTURA DEL REPOSITORIO

```
pipeline_didi/
│
├── main.py                          # Script de ingesta y procesamiento
├── README.md                        # Este archivo (Arquitectura)
│
├── data/
│   ├── raw/
│   │   └── didi_analisis_12_01.csv  # Dataset original (26 registros)
│   └── processed/
│       └── didi_procesado.csv       # Dataset limpio + derivadas (24 columnas)
│
├── sql/
│   └── ANALISIS_SQL_FINAL.sql       # Scripts para MySQL 8.0
│
└── docs/
    ├── DICCIONARIO_VARIABLES.md     # 22 variables (9 primarias, 13 derivadas)
    ├── METODOLOGIA.md               # Protocolo de recolección y auditoría
    ├── RESULTADOS.md                # 10 tablas de análisis
    └── CORRECCION_AUDITORIA.md      # Ajustes de métricas financieras
```

---

## 🚀 INSTALACIÓN Y USO

### Requisitos

- **Python:** 3.14+ (compatible con 3.10+)
- **Librerías:** pandas, numpy
- **Sistema Operativo:** Windows, macOS, Linux
- **MySQL:** 8.0+ (opcional, solo para análisis SQL)

### Instalación

```bash
# Clonar repositorio (si está en Git)
git clone https://github.com/tu-usuario/pipeline_didi.git
cd pipeline_didi

# Instalar dependencias
pip install pandas numpy --break-system-packages

# Verificar estructura de archivos
ls -R
```

### Uso Básico

#### 1. Ejecutar Pipeline de Ingesta

```bash
python3 main.py
```

**Salida esperada:**
```
======================================================================
PIPELINE DE AUDITORÍA - ARBITRAJE ALGORÍTMICO DIDI FOOD
======================================================================

📂 Directorio Base: /home/usuario/pipeline_didi
📥 Archivo Entrada: data/raw/didi_analisis_12_01.csv
📤 Archivo Salida: data/processed/didi_procesado.csv

🔄 [PASO 1/5] Cargando datos raw...
✅ Cargados 26 registros

🧹 [PASO 2/5] Limpiando valores de kilómetros...
✅ Limpieza completada
   - KM Google total: 1571.38 km
   - KM DiDi total: 2601.89 km

📊 [PASO 3/5] Calculando métricas derivadas...
✅ Generadas 13 variables derivadas

🔍 [PASO 4/5] Generando reporte de auditoría...

======================================================================
MÉTRICAS GLOBALES DE AUDITORÍA (N=26)
======================================================================
💰 Total Ingresos:        $4,440,530 COP
💸 Total Gastos:          $431,000 COP
💵 Utilidad Neta:         $4,009,530 COP
📈 ROI Global:            930.28%
🔢 Múltiplo de Ingreso:   10.30x
🛣️  RO Global:             1.66x
======================================================================

💾 [PASO 5/5] Exportando datos procesados...
✅ Archivo exportado exitosamente
```

#### 2. Cargar a MySQL (Opcional)

```bash
mysql -u root -p < sql/ANALISIS_SQL_FINAL.sql
```

#### 3. Ver Resultados

```bash
# Ver tablas de análisis
cat docs/RESULTADOS.md

# Ver diccionario de variables
cat docs/DICCIONARIO_VARIABLES.md
```

---

## 📊 RESULTADOS CLAVE

### Métricas Globales (Valores Auditados)

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **N (Registros)** | 26 días | Periodo: 2025-12-05 a 2026-01-31 |
| **Total Ingresos** | $4,440,530 COP | Ingresos garantizados por DiDi |
| **Total Gastos** | $431,000 COP | Gastos operativos reales (ajustado) |
| **Utilidad Neta** | $4,009,530 COP | Ganancia después de gastos |
| **ROI Global** | 930.28% | Cada peso genera $10.30 COP |
| **RO Global** | 1.66x | DiDi calcula rutas 66% más largas |
| **Múltiplo de Ingreso** | 10.30x | Ingresos / Gastos |

### Insights Clave

1. **Alta Rentabilidad:** ROI de 930.28% confirma modelo de negocio altamente rentable.
2. **Asimetría Confirmada:** DiDi calcula rutas 66% más largas que Google Maps.
3. **Oportunidad de Arbitraje:** Ahorrar 39.6 km/día usando rutas de Google.
4. **Anomalías Documentadas:** 6 días con gasto $0 (error de registro).
5. **Turnos Óptimos:** Duraciones de 10-13 horas maximizan ingreso/hora.

### Diferenciación Semántica

⚠️ **ADVERTENCIA:** No confundir estas métricas:

| Métrica | Uso | Fórmula | Valor |
|---------|-----|---------|-------|
| **RO (Ratio de Optimización)** | Eficiencia de distancia | `km_didi / km_google` | **1.66x** |
| **Múltiplo de Ingreso** | Relación financiera | `Ingresos / Gastos` | **10.30x** |

---

## 📚 DOCUMENTACIÓN TÉCNICA

### Documentos Principales

1. **DICCIONARIO_VARIABLES.md**
   - 22 variables definidas (9 primarias, 13 derivadas)
   - Fórmulas exactas para cada métrica
   - Tipos de datos y validaciones

2. **METODOLOGIA.md**
   - Protocolo de recolección de datos
   - Tratamiento de medianoche (Día Operativo)
   - Definición de asimetría topológica
   - Filtro Cognitivo del Operador
   - Limitaciones del estudio

3. **RESULTADOS.md**
   - 10 tablas de análisis
   - Dashboard ejecutivo
   - Top 5 mejores/peores días
   - Análisis de anomalías

4. **CORRECCION_AUDITORIA.md**
   - Ajuste de gastos: $399,500 → $431,000 COP
   - Corrección de ROI: 1,003.64% → 930.28%
   - Ajuste de RO: 1.71x → 1.66x

5. **ANALISIS_SQL_FINAL.sql**
   - Definición de tabla `didi_operaciones`
   - 10 vistas de análisis
   - Scripts de consulta

### Variables Clave

#### Variables Primarias (9)
- `fecha`, `h_inicio`, `h_fin`
- `km_google`, `km_didi`
- `garantizado_meta`, `ingreso_base`, `complemento_bono`
- `pedidos_fisicos`, `unidades_progreso`, `gastos_operativos`

#### Variables Derivadas (13)
- `duracion_horas` (con tratamiento de medianoche)
- `utilidad_neta`
- `ratio_optimizacion` (RO)
- `km_por_pedido_google`, `km_por_pedido_didi`
- `ingreso_por_hora`, `utilidad_por_hora`
- `roi_diario`, `rentabilidad_binaria`
- ... y más

---

## 🛡️ CONSIDERACIONES ÉTICAS

### Transparencia con DiDi

Este análisis **NO implica:**
- Evasión de políticas de DiDi
- Falsificación de ubicaciones
- Incumplimiento de contratos

El operador:
- Completa todas las entregas
- Sigue rutas legales y seguras
- No hackea el sistema

### Uso de Datos

- Los datos son propiedad del operador (registros personales).
- No se revelan datos personales ni direcciones de clientes.
- DiDi App solo proporciona métricas agregadas.

### Privacidad

- No se exponen ubicaciones GPS precisas.
- Solo métricas agregadas y anonimizadas.

---

## 🔧 MANEJO DE CASOS ESPECIALES

### 1. Turnos con Cruce de Medianoche

**Problema:**  
Si un turno comienza a las 17:01 y termina a las 0:12, el cálculo ingenuo daría `-16:49` horas.

**Solución:**  
Implementamos el concepto de **"Día Operativo"** como unidad indivisible. Si `h_fin < h_inicio`, sumamos 24 horas:

```python
if minutos_fin < minutos_inicio:
    minutos_fin += 1440  # +24 horas
```

**Resultado:** `17:01 a 0:12` → `7.18 horas` (correcto)

**Casos en dataset:** 4 turnos (15.4% del total)

### 2. Días con Gasto $0

**Observación:** 6 días registran `gastos_operativos = 0`

**Tratamiento:**
- ROI diario: No calculable (`NaN`)
- Utilidad neta: Se registra normalmente
- Clasificación: Anomalía técnica documentada

**Decisión:** Reportar anomalía, **NO** excluir registros.

### 3. Manejo de Windows MAX_PATH

El script usa `pathlib.Path` para manejar rutas largas en Windows sin errores de `MAX_PATH`.

---

## 📈 PRÓXIMOS PASOS

### Mejoras Futuras

1. **Visualización:**
   - Gráficos de dispersión (RO vs Utilidad)
   - Heatmap de rentabilidad por hora del día
   - Dashboard interactivo con Streamlit

2. **Análisis Avanzado:**
   - Segmentación por franja horaria (mañana/tarde/noche)
   - Análisis de estacionalidad (días festivos)
   - Predicción de ingresos con Machine Learning

3. **Automatización:**
   - Scraping automático de DiDi App
   - Integración con Google Maps API
   - Alertas de anomalías en tiempo real

4. **Escalabilidad:**
   - Análisis multi-operador
   - Comparación entre ciudades
   - Benchmarking con otras plataformas (Rappi, Uber Eats)

---

## 🤝 CONTRIBUCIONES

Este proyecto es **Open Source** bajo licencia MIT. Contribuciones son bienvenidas:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📜 LICENCIA Y ATRIBUCIONES

### Licencia

MIT License - Copyright (c) 2026

### Atribuciones

- **Autor:** Ingeniero de Datos Senior
- **Datos:** Operador de DiDi Food, Bogotá D.C., Colombia
- **Tecnologías:** Python 3.14, pandas, numpy, MySQL 8.0
- **Filosofía:** Transparencia Radical (inspirado en Ray Dalio)

---

## 📞 CONTACTO

Para preguntas, comentarios o colaboraciones:

- **Email:** [felipecastro933@gmail.com] [ifcastrop@udistrital.edu.co]
- **GitHub:** [Buckethead9]
- **LinkedIn:** [https://www.linkedin.com/in/ivanfelipecastropinzon/]

---

## 🎓 CITA RECOMENDADA

Si usas este proyecto en investigación o análisis, cita como:

```
Pipeline de Auditoría - Arbitraje Algorítmico DiDi Food (2026).
Autor: Ivan Felipe Castro Pinzón.
Versión 1.0.0.
Disponible en: [https://github.com/buckethead9/didi-algorithmic-arbitrage]
```

---

## ⚖️ DECLARACIÓN DE INTEGRIDAD

> "Este pipeline no busca perfección estética, busca fidelidad técnica.  
> Un ROI de 930% basado en datos reales es más valioso que un ROI de 1,000% basado en omisiones.  
> Las anomalías se documentan, no se ocultan.  
> La verdad por encima de la armonía."

**Firmado:**  
*Pipeline de Auditoría de Integridad v1.0*  
*Fecha: 2026-02-13*

---

**🚀 ¡Comienza tu análisis ahora!**

```bash
python3 main.py
```
