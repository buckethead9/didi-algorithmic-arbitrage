-- ============================================================================
-- ANÁLISIS MCKINSEY: ARBITRAJE ALGORÍTMICO EN LOGÍSTICA ÚLTIMA MILLA
-- Periodo: Diciembre 2025 - Enero 2026 (25 días operativos)
-- Ratio de Optimización Global: 1.65x
-- ============================================================================

CREATE DATABASE IF NOT EXISTS didi_operaciones
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

USE didi_operaciones;

-- ============================================================================
-- TABLA BASE: 9 Variables Minimalistas McKinsey
-- ============================================================================

DROP TABLE IF EXISTS registros_didi;

CREATE TABLE registros_didi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    h_inicio TIME NOT NULL COMMENT 'Hora primer pedido aceptado',
    h_fin TIME NOT NULL COMMENT 'Hora candado en casa',
    km_google_maps DECIMAL(10,2) NOT NULL COMMENT 'KM reales pedaleados',
    km_didi_app DECIMAL(10,2) NOT NULL COMMENT 'KM reportados por DiDi',
    ingreso_bruto DECIMAL(10,2) NOT NULL COMMENT 'Ganancia total garantizada',
    pedidos_cohete INT NOT NULL COMMENT 'Pedidos ≥7km (cuentan x2)',
    pedidos_normales INT NOT NULL COMMENT 'Pedidos <7km',
    gasto_extra DECIMAL(10,2) DEFAULT 0 COMMENT 'Gastos operativos',
    
    INDEX idx_fecha (fecha),
    INDEX idx_ratio (km_didi_app, km_google_maps)
) ENGINE=InnoDB COMMENT='Datos dic-ene 2025-2026';

-- ============================================================================
-- CARGA DE DATOS (25 días)
-- ============================================================================

INSERT INTO registros_didi 
(fecha, h_inicio, h_fin, km_google_maps, km_didi_app, ingreso_bruto, pedidos_cohete, pedidos_normales, gasto_extra)
VALUES
('2025-12-05', '17:05', '23:23', 45.06, 88.60, 130000, 11, 1, 17000),
('2025-12-06', '13:34', '23:56', 72.58, 120.70, 188000, 15, 0, 17000),
('2025-12-07', '12:47', '23:25', 66.79, 122.50, 229000, 14, 3, 18000),
('2025-12-08', '11:36', '23:18', 104.61, 135.40, 209000, 17, 0, 21000),
('2025-12-13', '12:27', '22:57', 63.08, 92.10, 143000, 10, 1, 58000),
('2025-12-14', '12:14', '23:56', 101.87, 139.40, 251000, 18, 0, 19000),
('2025-12-20', '12:45', '23:05', 102.02, 146.80, 263000, 18, 2, 16000),
('2025-12-21', '13:33', '23:51', 94.75, 135.10, 268000, 18, 0, 21500),
('2025-12-23', '16:41', '22:06', 33.69, 51.50, 73000, 6, 2, 16000),
('2025-12-24', '17:02', '21:56', 54.64, 76.20, 132000, 8, 2, 0),
('2025-12-25', '12:36', '23:19', 86.50, 144.70, 302000, 12, 9, 14000),
('2025-12-27', '11:58', '22:24', 72.20, 106.30, 185000, 9, 6, 19000),
('2025-12-28', '12:20', '23:18', 85.34, 136.20, 283000, 13, 5, 15000),
('2025-12-31', '17:07', '23:42', 54.41, 81.20, 125000, 10, 3, 0),
('2026-01-01', '15:34', '23:46', 57.91, 96.90, 183000, 12, 5, 0),
('2026-01-04', '11:42', '23:22', 42.74, 67.90, 114000, 8, 7, 18000),
('2026-01-08', '18:10', '21:51', 11.16, 17.70, 31000, 3, 0, 0),
('2026-01-10', '12:22', '22:49', 48.25, 75.70, 147000, 12, 0, 17000),
('2026-01-11', '11:45', '23:04', 60.38, 104.70, 244000, 18, 0, 0),
('2026-01-12', '15:48', '22:33', 35.24, 50.40, 104000, 7, 2, 20000),
('2026-01-17', '15:47', '21:47', 30.96, 53.30, 119000, 10, 1, 16000),
('2026-01-18', '13:33', '22:44', 43.98, 87.50, 206500, 17, 2, 21000),
('2026-01-24', '18:47', '22:02', 19.79, 30.70, 47500, 3, 3, 18000),
('2026-01-25', '13:33', '21:42', 46.07, 73.50, 169500, 15, 1, 0),
('2026-01-30', '11:56', '18:15', 28.70, 54.20, 132530, 0, 0, 0);

-- ============================================================================
-- MOTOR MCKINSEY: Agregar Columnas Calculadas
-- ============================================================================

ALTER TABLE registros_didi
ADD COLUMN tiempo_total_horas DECIMAL(5,2) COMMENT 'Duración h_inicio a h_fin',
ADD COLUMN pedidos_totales INT COMMENT 'Suma cohete + normales',
ADD COLUMN ratio_optimizacion DECIMAL(5,2) COMMENT 'km_didi / km_google (RO)',
ADD COLUMN utilidad_neta DECIMAL(10,2) COMMENT 'ingreso - gasto - desgaste_bici',
ADD COLUMN ingreso_por_km_real DECIMAL(8,2) COMMENT 'utilidad / km_google',
ADD COLUMN velocidad_enganche DECIMAL(5,1) COMMENT 'minutos por pedido',
ADD COLUMN velocidad_operativa DECIMAL(5,2) COMMENT 'km/h operativa',
ADD COLUMN salario_efectivo_hora DECIMAL(8,2) COMMENT 'utilidad / tiempo',
ADD COLUMN eficiencia_cohete_pct DECIMAL(5,2) COMMENT '% pedidos cohete';

-- ============================================================================
-- CALCULAR TODAS LAS MÉTRICAS DERIVADAS
-- ============================================================================

UPDATE registros_didi
SET 
    -- Tiempo total
    tiempo_total_horas = TIMESTAMPDIFF(MINUTE, 
        CONCAT(fecha, ' ', h_inicio), 
        CONCAT(fecha, ' ', h_fin)
    ) / 60.0,
    
    -- Pedidos totales
    pedidos_totales = pedidos_cohete + pedidos_normales,
    
    -- Ratio de Optimización (RO)
    ratio_optimizacion = ROUND(km_didi_app / NULLIF(km_google_maps, 0), 2),
    
    -- Utilidad Neta (desgaste bici = $124/km)
    utilidad_neta = ingreso_bruto - gasto_extra - (km_google_maps * 124),
    
    -- Ingreso por KM real
    ingreso_por_km_real = ROUND(
        (ingreso_bruto - gasto_extra) / NULLIF(km_google_maps, 0), 
        2
    ),
    
    -- Velocidad de Enganche (min/pedido)
    velocidad_enganche = ROUND(
        TIMESTAMPDIFF(MINUTE, 
            CONCAT(fecha, ' ', h_inicio), 
            CONCAT(fecha, ' ', h_fin)
        ) / NULLIF(pedidos_cohete + pedidos_normales, 0),
        1
    ),
    
    -- Velocidad Operativa (km/h)
    velocidad_operativa = ROUND(
        km_google_maps / NULLIF(
            TIMESTAMPDIFF(MINUTE, 
                CONCAT(fecha, ' ', h_inicio), 
                CONCAT(fecha, ' ', h_fin)
            ) / 60.0,
            0
        ),
        2
    ),
    
    -- Salario Efectivo por Hora
    salario_efectivo_hora = ROUND(
        (ingreso_bruto - gasto_extra - (km_google_maps * 124)) / NULLIF(
            TIMESTAMPDIFF(MINUTE, 
                CONCAT(fecha, ' ', h_inicio), 
                CONCAT(fecha, ' ', h_fin)
            ) / 60.0,
            0
        ),
        2
    ),
    
    -- Eficiencia Cohete %
    eficiencia_cohete_pct = ROUND(
        (pedidos_cohete / NULLIF(pedidos_cohete + pedidos_normales, 0)) * 100,
        2
    );

-- ============================================================================
-- VISTAS ANALÍTICAS
-- ============================================================================

-- VISTA 1: Resumen Ejecutivo
CREATE OR REPLACE VIEW v_resumen_ejecutivo AS
SELECT 
    'PERIODO' AS metrica,
    CONCAT(MIN(fecha), ' → ', MAX(fecha)) AS valor
FROM registros_didi
UNION ALL
SELECT 'DÍAS OPERATIVOS', CAST(COUNT(*) AS CHAR) FROM registros_didi
UNION ALL
SELECT 'KM REALES PEDALEADOS', CONCAT(FORMAT(SUM(km_google_maps), 1), ' km') FROM registros_didi
UNION ALL
SELECT 'KM REPORTADOS DIDI', CONCAT(FORMAT(SUM(km_didi_app), 1), ' km') FROM registros_didi
UNION ALL
SELECT '🚀 RATIO OPTIMIZACIÓN', CONCAT(FORMAT(SUM(km_didi_app) / SUM(km_google_maps), 2), 'x') FROM registros_didi
UNION ALL
SELECT 'INGRESO TOTAL', CONCAT('$', FORMAT(SUM(ingreso_bruto), 0)) FROM registros_didi
UNION ALL
SELECT 'GASTOS TOTALES', CONCAT('$', FORMAT(SUM(gasto_extra), 0)) FROM registros_didi
UNION ALL
SELECT 'DESGASTE BICI', CONCAT('$', FORMAT(SUM(km_google_maps * 124), 0)) FROM registros_didi
UNION ALL
SELECT 'UTILIDAD NETA', CONCAT('$', FORMAT(SUM(utilidad_neta), 0)) FROM registros_didi
UNION ALL
SELECT 'SALARIO/HORA PROM', CONCAT('$', FORMAT(AVG(salario_efectivo_hora), 0)) FROM registros_didi;

-- VISTA 2: Top 10 Mejores Días (por salario/hora)
CREATE OR REPLACE VIEW v_top_10_dias AS
SELECT 
    fecha,
    ratio_optimizacion AS ro,
    salario_efectivo_hora AS salario_hora,
    utilidad_neta,
    eficiencia_cohete_pct AS cohetes_pct,
    km_google_maps AS km_reales,
    pedidos_totales
FROM registros_didi
WHERE salario_efectivo_hora IS NOT NULL
ORDER BY salario_efectivo_hora DESC
LIMIT 10;

-- VISTA 3: Análisis por Nivel de RO
CREATE OR REPLACE VIEW v_analisis_por_ro AS
SELECT 
    CASE 
        WHEN ratio_optimizacion >= 2.0 THEN '🚀 Excelente (≥2.0x)'
        WHEN ratio_optimizacion >= 1.5 THEN '🟢 Bueno (1.5-2.0x)'
        WHEN ratio_optimizacion >= 1.0 THEN '🟡 Neutro (1.0-1.5x)'
        ELSE '🔴 Malo (<1.0x)'
    END AS nivel_ro,
    COUNT(*) AS dias,
    ROUND(AVG(ratio_optimizacion), 2) AS ro_promedio,
    ROUND(AVG(salario_efectivo_hora), 0) AS salario_promedio,
    ROUND(AVG(utilidad_neta), 0) AS utilidad_promedio
FROM registros_didi
WHERE ratio_optimizacion IS NOT NULL
GROUP BY nivel_ro
ORDER BY ro_promedio DESC;

-- VISTA 4: Impacto Cohetes en Utilidad
CREATE OR REPLACE VIEW v_cohetes_vs_utilidad AS
SELECT 
    CASE 
        WHEN eficiencia_cohete_pct >= 80 THEN '≥80% cohetes'
        WHEN eficiencia_cohete_pct >= 60 THEN '60-79% cohetes'
        WHEN eficiencia_cohete_pct >= 40 THEN '40-59% cohetes'
        ELSE '<40% cohetes'
    END AS nivel_cohetes,
    COUNT(*) AS dias,
    ROUND(AVG(utilidad_neta), 0) AS utilidad_promedio,
    ROUND(AVG(ratio_optimizacion), 2) AS ro_promedio,
    ROUND(AVG(salario_efectivo_hora), 0) AS salario_promedio
FROM registros_didi
WHERE eficiencia_cohete_pct IS NOT NULL
GROUP BY nivel_cohetes
ORDER BY AVG(eficiencia_cohete_pct) DESC;

-- ============================================================================
-- CONSULTAS DE ANÁLISIS (Ejecutar una por una)
-- ============================================================================

-- ANÁLISIS 1: Resumen Ejecutivo
SELECT * FROM v_resumen_ejecutivo;

-- ANÁLISIS 2: Top 10 Mejores Días
SELECT * FROM v_top_10_dias;

-- ANÁLISIS 3: Distribución por Ratio de Optimización
SELECT * FROM v_analisis_por_ro;

-- ANÁLISIS 4: Impacto de Cohetes en Utilidad
SELECT * FROM v_cohetes_vs_utilidad;

-- ANÁLISIS 5: Comparación Mayor vs Menor RO
(SELECT 
    'Top 5 Mayor RO' AS grupo,
    fecha,
    ratio_optimizacion AS ro,
    salario_efectivo_hora AS salario_h,
    km_google_maps AS km_reales,
    km_didi_app AS km_app
FROM registros_didi
WHERE ratio_optimizacion IS NOT NULL
ORDER BY ratio_optimizacion DESC
LIMIT 5)

UNION ALL

(SELECT 
    'Top 5 Menor RO',
    fecha,
    ratio_optimizacion,
    salario_efectivo_hora,
    km_google_maps,
    km_didi_app
FROM registros_didi
WHERE ratio_optimizacion IS NOT NULL
ORDER BY ratio_optimizacion ASC
LIMIT 5);

-- ANÁLISIS 6: Tendencia Mensual
SELECT 
    DATE_FORMAT(fecha, '%Y-%m') AS mes,
    COUNT(*) AS dias_trabajados,
    ROUND(AVG(ratio_optimizacion), 2) AS ro_promedio,
    ROUND(AVG(salario_efectivo_hora), 0) AS salario_promedio,
    FORMAT(SUM(utilidad_neta), 0) AS utilidad_total
FROM registros_didi
GROUP BY mes
ORDER BY mes;

-- ANÁLISIS 7: Detalle KM Reales vs Reportados
SELECT 
    fecha,
    km_google_maps AS km_reales,
    km_didi_app AS km_reportados,
    ROUND(km_didi_app - km_google_maps, 1) AS km_diferencia,
    ratio_optimizacion AS ro,
    CONCAT(ROUND((km_didi_app - km_google_maps) / km_google_maps * 100, 0), '%') AS ventaja_pct
FROM registros_didi
WHERE km_google_maps > 0
ORDER BY ratio_optimizacion DESC;

-- ANÁLISIS 8: Eficiencia Temporal
SELECT 
    fecha,
    TIME_FORMAT(h_inicio, '%H:%i') AS inicio,
    TIME_FORMAT(h_fin, '%H:%i') AS fin,
    tiempo_total_horas AS horas,
    pedidos_totales,
    velocidad_enganche AS min_pedido,
    velocidad_operativa AS km_h,
    salario_efectivo_hora AS salario_h
FROM registros_didi
ORDER BY salario_efectivo_hora DESC;

-- ANÁLISIS 9: ROI y Rentabilidad
SELECT 
    FORMAT(SUM(ingreso_bruto), 0) AS ingreso_total,
    FORMAT(SUM(gasto_extra), 0) AS gastos_totales,
    FORMAT(SUM(km_google_maps * 124), 0) AS desgaste_total,
    FORMAT(SUM(utilidad_neta), 0) AS utilidad_neta_total,
    CONCAT(
        ROUND((SUM(utilidad_neta) / (SUM(gasto_extra) + SUM(km_google_maps * 124))) * 100, 2),
        '%'
    ) AS roi_porcentaje
FROM registros_didi;

-- ANÁLISIS 10: Tendencia Semanal
SELECT 
    CONCAT('Semana ', WEEK(fecha)) AS semana,
    COUNT(*) AS dias,
    ROUND(AVG(ratio_optimizacion), 2) AS ro_promedio,
    ROUND(AVG(salario_efectivo_hora), 0) AS salario_promedio,
    FORMAT(SUM(utilidad_neta), 0) AS utilidad_semanal
FROM registros_didi
GROUP BY WEEK(fecha)
ORDER BY MIN(fecha);

-- ============================================================================
-- MÉTRICAS CLAVE PARA TESIS
-- ============================================================================

-- ¿Cuál es el RO promedio por eficiencia de cohetes?
SELECT 
    CASE 
        WHEN eficiencia_cohete_pct >= 90 THEN '≥90%'
        WHEN eficiencia_cohete_pct >= 70 THEN '70-89%'
        WHEN eficiencia_cohete_pct >= 50 THEN '50-69%'
        ELSE '<50%'
    END AS rango_cohetes,
    COUNT(*) AS dias,
    ROUND(AVG(ratio_optimizacion), 2) AS ro_promedio,
    ROUND(AVG(ingreso_por_km_real), 0) AS ingreso_km_promedio
FROM registros_didi
WHERE eficiencia_cohete_pct IS NOT NULL
GROUP BY rango_cohetes
ORDER BY AVG(eficiencia_cohete_pct) DESC;

-- Correlación: ¿Más KM reales = Mayor RO?
SELECT 
    CASE 
        WHEN km_google_maps >= 80 THEN '≥80 km'
        WHEN km_google_maps >= 60 THEN '60-79 km'
        WHEN km_google_maps >= 40 THEN '40-59 km'
        ELSE '<40 km'
    END AS rango_km,
    COUNT(*) AS dias,
    ROUND(AVG(ratio_optimizacion), 2) AS ro_promedio,
    ROUND(AVG(velocidad_operativa), 1) AS vel_promedio_km_h
FROM registros_didi
GROUP BY rango_km
ORDER BY AVG(km_google_maps) DESC;

-- ============================================================================
-- FIN DEL ANÁLISIS
-- ============================================================================
