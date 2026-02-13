# 🚀 DiDi Algorithmic Arbitrage: Optimization & Audit Pipeline

**Análisis de asimetría logística:** Explotando la brecha entre la infraestructura urbana (ciclorrutas) y el ruteo algorítmico motorizado.

---

## 🧠 Tesis del Proyecto

Este repositorio actúa como un **amplificador cognitivo** para auditar el "Arbitraje Algorítmico". La hipótesis confirmada es que el algoritmo de ruteo de la plataforma (diseñado para vehículos motorizados) sobreestima las distancias en entornos urbanos densos, permitiendo que un operador en bicicleta genere kilómetros "fantasma" mediante el uso de atajos e infraestructura no motorizada.

---

## 📊 Indicadores Maestros (Fuente de Verdad)

| Métrica | Valor Real | Significado |
|---------|------------|-------------|
| **Ratio de Optimización (RO)** | **1.71x** | Por cada 1km físico, se liquidan 1.71km algorítmicos. |
| **Utilidad Neta Total** | **$4,009,530** | Beneficio real tras auditar 24 días operativos. |
| **Eficiencia de Arbitraje** | **83.4%** | Tasa de éxito en la captura de "pedidos cohete" (≥7km). |
| **ROI Operativo** | **2,479%** | Retorno sobre el gasto operativo (insumos/mantenimiento). |

---

## 🛠️ Pipeline de Datos

El sistema está construido para **eliminar el ruido cognitivo** mediante tres capas de procesamiento:

### 1. Ingesta (Python 3.14)
Limpieza de strings y normalización de datos crudos (`data/raw`). Configurado para manejar rutas largas de Windows (MAX_PATH).

```python
# Procesamiento de datos crudos
python main.py data/raw/didi_diciembre_enero_COMPLETO.csv
```

### 2. Auditoría (SQL)
Clasificación de servicios en "Arbitraje Agresivo" o "Optimización Estándar" mediante lógica de negocio inmutable.

```sql
-- Definición de Arbitraje Agresivo
SELECT 
    fecha,
    (km_didi_app / km_google_maps) AS ratio_optimizacion,
    CASE 
        WHEN (km_didi_app / km_google_maps) >= 1.5 THEN 'Arbitraje Agresivo'
        ELSE 'Optimización Estándar'
    END AS estrategia_status
FROM didi_operaciones
WHERE ratio_optimizacion IS NOT NULL;
```

### 3. Visualización (Power BI)
Conectado vía Web/Raw para monitoreo dinámico de la asimetría.

---

## 📁 Estructura del Repositorio

```
📦 didi-algorithmic-arbitrage/
├── 📄 main.py                    # Pipeline de procesamiento Python
├── 📄 README.md                  # Este archivo
│
├── 📁 data/
│   ├── 📁 raw/                   # Datos originales sin procesar
│   │   └── didi_diciembre_enero_COMPLETO.csv
│   └── 📁 processed/             # Datos auditados y limpios
│       └── didi_procesado.csv
│
├── 📁 sql/
│   └── ANALISIS_SQL_FINAL.sql    # Scripts de auditoría y vistas
│
└── 📁 docs/
    ├── DICCIONARIO_VARIABLES.md  # Definiciones técnicas
    ├── METODOLOGIA.md             # Marco metodológico
    └── RESULTADOS.md              # Análisis detallado
```

---

## 📈 Hallazgos Clave (La Verdad sin Filtros)

### 1. Asimetría de Distancia
**987 km adicionales** pagados por el algoritmo que no requirieron esfuerzo físico real.

```
KM Reales Pedaleados:     1,526 km
KM Reportados por DiDi:   2,513 km
────────────────────────────────
KM Fantasma:                987 km (65% extra)
```

### 2. Sensibilidad al Rango
Los pedidos de larga distancia (≥7km) incrementan el RO en un **15.4% promedio** frente a pedidos cortos.

| Tipo de Pedido | RO Promedio | Utilidad/Pedido |
|----------------|-------------|-----------------|
| Cohete (≥7km) | 1.78x | $18,500 |
| Normal (<7km) | 1.54x | $12,300 |

### 3. Volatilidad Operativa
El sistema detectó una desviación estándar de **$74,650**, lo que clasifica la operación como "**Alto Riesgo / Alta Recompensa**".

---

## 🚀 Instalación y Uso

### Requisitos
```bash
Python 3.8+
pandas >= 1.5.0
numpy >= 1.24.0
MySQL 8.0+
```

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/buckethead9/didi-algorithmic-arbitrage.git
cd didi-algorithmic-arbitrage

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear estructura de directorios
mkdir -p data/raw data/processed sql
```

### Ejecución del Pipeline

```bash
# Procesar datos crudos
python main.py data/raw/didi_diciembre_enero_COMPLETO.csv

# Salida esperada:
# ✓ 24 registros válidos
# ✓ RO Global: 1.71x
# ✓ Utilidad: $4,009,530
# ✓ Datos guardados en: data/processed/didi_procesado.csv
```

### Análisis SQL

```bash
# Importar base de datos
mysql -u root -p < sql/ANALISIS_SQL_FINAL.sql

# Ejecutar análisis
mysql -u root -p didi_operaciones -e "SELECT * FROM v_resumen_ejecutivo;"
```

---

## 📊 Análisis Disponibles

El sistema incluye **10 análisis predefinidos** en SQL:

1. ✅ Resumen Ejecutivo
2. ✅ Top 10 Mejores Días
3. ✅ Distribución por RO
4. ✅ Impacto de Cohetes en Utilidad
5. ✅ Comparación Mayor vs Menor RO
6. ✅ Tendencia Mensual
7. ✅ KM Reales vs Reportados (Detalle)
8. ✅ Eficiencia Temporal
9. ✅ ROI y Rentabilidad
10. ✅ Tendencia Semanal

---

## 🎯 Casos de Uso

### Para Ingenieros de Datos
- Ejemplo de pipeline ETL completo en Python
- Limpieza de datos sucios (strings con formatos mixtos)
- Cálculo de métricas derivadas
- Validación de integridad de datos

### Para Analistas
- Sistema de clasificación de estrategias operativas
- Análisis de correlaciones (RO vs Utilidad)
- Detección de patrones temporales

### Para Tesis/Investigación
- Marco metodológico completo documentado
- Dataset real con 24 días operativos
- Métricas validadas y reproducibles

---

## 🔬 Metodología

### Variables Primarias (9)
```
fecha, h_inicio, h_fin,
km_google_maps, km_didi_app,
ingreso_bruto, pedidos_cohete, pedidos_normales,
gasto_extra
```

### Variables Derivadas (13)
```
tiempo_total_horas, pedidos_totales,
ratio_optimizacion, estrategia_status,
utilidad_neta, ingreso_por_km_real,
velocidad_enganche, velocidad_operativa,
salario_efectivo_hora, eficiencia_cohete_pct
... + variables de clasificación
```

Ver documentación completa en [`docs/DICCIONARIO_VARIABLES.md`](docs/DICCIONARIO_VARIABLES.md)

---

## 📄 Documentación

- **[METODOLOGIA.md](docs/METODOLOGIA.md)** - Diseño del estudio, protocolo de recolección
- **[RESULTADOS.md](docs/RESULTADOS.md)** - Análisis detallado, correlaciones, conclusiones
- **[DICCIONARIO_VARIABLES.md](docs/DICCIONARIO_VARIABLES.md)** - 22 variables documentadas con fórmulas

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-metrica`)
3. Commit cambios (`git commit -m 'feat: Agregar métrica X'`)
4. Push (`git push origin feature/nueva-metrica`)
5. Abre un Pull Request

---

## 📝 Citación

Si usas este dataset en investigación académica:

```bibtex
@misc{castro2026didi,
  author = {Castro Pinzón, Iván Felipe},
  title = {DiDi Algorithmic Arbitrage: Audit Pipeline},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/buckethead9/didi-logistics-optimization}
}
```

---

## 📞 Contacto y Autoría

**Autor:** Iván Felipe Castro Pinzón  
**LinkedIn:** https://www.linkedin.com/in/ivanfelipecastropinzon/  
**Email:** felipecastro933@gmail.com -- ifcastrop@udistrital.edu.co
**Proyecto:** Logistics Optimization & Algorithmic Arbitrage v2.0

---

## 📄 Licencia

MIT License - Ver `LICENSE` para detalles

---

## ⚠️ Disclaimer

Este análisis es con fines académicos y de investigación. Los datos son reales pero anonimizados. No se promueve la violación de términos de servicio de plataformas digitales.

---

**Última actualización:** Febrero 2026  
**Versión:** 2.0.0  
**Status:** ✅ Producción - Pipeline Validado
