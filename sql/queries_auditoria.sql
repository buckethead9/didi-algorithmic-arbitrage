-- ============================================================================
-- QUERIES DE AUDITORÍA — DSS v1.2
-- DiDi Food · San Cristóbal Sur · Bogotá D.C.
-- MySQL 8.0+ · Umbrales CASE sincronizados con app_copiloto.py y main.py
-- ============================================================================
-- INVARIANTES (no modificar sin actualizar main.py y app_copiloto.py):
--   ROI Auditado:    782.24%  (N_válido=20, WHERE gastos_operativos > 0)
--   RO Media:        1.706x
--   Zona Óptima:     1.73 ≤ RO ≤ 1.84
--   Zona Crítica:    RO ≥ 2.0
--   β modelo:        $14,940 COP/pedido
--   Franja PICO:     17:00 – 20:59
-- ============================================================================

-- ─── 1. CREACIÓN DE TABLA BASE ──────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS didi_procesado_v1 (
    -- Dimensión 1: Tiempo-Identificación
    fecha                   DATE            NOT NULL,
    h_inicio                VARCHAR(5)      NOT NULL COMMENT 'Formato HH:MM',
    h_fin                   VARCHAR(5)      NOT NULL COMMENT 'Formato HH:MM — puede ser 00:xx (cruce medianoche)',
    duracion_horas          DECIMAL(5,2)    NOT NULL,
    franja_pico             TINYINT(1)      NOT NULL COMMENT '1 si 17:00 ≤ h_inicio < 21:00',

    -- Dimensión 2: Distancia
    km_google               DECIMAL(8,2)    NOT NULL,
    km_didi                 DECIMAL(8,2)    NOT NULL,
    km_fantasma             DECIMAL(8,2)    GENERATED ALWAYS AS (km_didi - km_google) STORED,
    ratio_optimizacion      DECIMAL(6,4)    GENERATED ALWAYS AS (km_didi / km_google) STORED,

    -- Dimensión 3: Ingreso MECE
    ingreso_base            INT             NOT NULL,
    complemento_bono        INT             NOT NULL,
    garantizado_meta        INT             GENERATED ALWAYS AS (ingreso_base + complemento_bono) STORED,
    proporcion_bono         DECIMAL(6,4)    GENERATED ALWAYS AS (complemento_bono / (ingreso_base + complemento_bono)) STORED,

    -- Dimensión 4: Costo e Integridad
    gastos_operativos       INT             NOT NULL DEFAULT 0,
    flag_gasto_cero         TINYINT(1)      GENERATED ALWAYS AS (IF(gastos_operativos = 0, 1, 0)) STORED,

    -- Dimensión 5: Resultado
    utilidad_neta           INT             GENERATED ALWAYS AS (ingreso_base + complemento_bono - gastos_operativos) STORED,
    utilidad_por_hora       DECIMAL(10,2)   NULL,
    roi_diario              DECIMAL(10,2)   NULL COMMENT 'NaN cuando gastos_operativos = 0 — preservado como NULL, no imputado',
    rentabilidad_binaria    TINYINT(1)      GENERATED ALWAYS AS (IF(ingreso_base + complemento_bono - gastos_operativos > 0, 1, 0)) STORED,

    -- Dimensión 6: Producción y Eficiencia
    pedidos_fisicos         INT             NOT NULL,
    unidades_progreso       INT             NOT NULL,
    eficiencia_cumplimiento DECIMAL(6,4)    GENERATED ALWAYS AS (unidades_progreso / pedidos_fisicos) STORED,
    km_por_pedido_google    DECIMAL(8,4)    GENERATED ALWAYS AS (km_google / pedidos_fisicos) STORED,
    km_por_pedido_didi      DECIMAL(8,4)    GENERATED ALWAYS AS (km_didi / pedidos_fisicos) STORED,
    ingreso_por_km_google   DECIMAL(10,2)   GENERATED ALWAYS AS ((ingreso_base + complemento_bono) / km_google) STORED,
    ingreso_por_hora        DECIMAL(10,2)   NULL,

    -- Dimensión 7: Feature Engineering DSS
    zona_arbitraje_optima   TINYINT(1)      GENERATED ALWAYS AS (IF(km_didi / km_google BETWEEN 1.73 AND 1.84, 1, 0)) STORED,
    alerta_critica          TINYINT(1)      GENERATED ALWAYS AS (IF(km_didi / km_google >= 2.0, 1, 0)) STORED,

    PRIMARY KEY (fecha),
    INDEX idx_ro (ratio_optimizacion),
    INDEX idx_franja (franja_pico),
    INDEX idx_zona (zona_arbitraje_optima),
    INDEX idx_alerta (alerta_critica)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Dataset procesado v1.1 · 28 variables MECE · DSS v1.2';


-- ─── 2. VISTA DIAGNÓSTICA — CLASIFICACIÓN OPERATIVA ─────────────────────────

CREATE OR REPLACE VIEW v_clasificacion_operativa AS
SELECT
    fecha,
    h_inicio,
    pedidos_fisicos,
    ROUND(km_didi / km_google, 4)  AS ratio_optimizacion,
    garantizado_meta,
    gastos_operativos,
    utilidad_neta,
    roi_diario,

    -- Franja horaria (sincronizada con main.py: PICO estrictamente [17:00, 21:00))
    CASE
        WHEN HOUR(STR_TO_DATE(h_inicio, '%H:%i')) BETWEEN 17 AND 20 THEN 'PICO'
        ELSE 'VALLE'
    END AS franja_horaria,

    -- Zona RO (5 categorías · sincronizadas con umbrales DSS)
    CASE
        WHEN km_didi / km_google < 1.30                              THEN 'Sub-activado'
        WHEN km_didi / km_google BETWEEN 1.30 AND 1.7299            THEN 'Neutra-Baja'
        WHEN km_didi / km_google BETWEEN 1.73 AND 1.84              THEN 'Arbitraje Óptimo'
        WHEN km_didi / km_google BETWEEN 1.8401 AND 1.9999          THEN 'Alta'
        WHEN km_didi / km_google >= 2.0                              THEN 'Crítica'
        ELSE 'Sin clasificar'
    END AS zona_ro,

    -- Decisión binarizada DSS
    CASE
        WHEN km_didi / km_google >= 2.0                              THEN 'NO OPERAR'
        WHEN km_didi / km_google BETWEEN 1.73 AND 1.84              THEN 'SÍ OPERAR'
        WHEN km_didi / km_google < 1.30                              THEN 'EVALUAR VIABILIDAD'
        ELSE 'MONITOREAR'
    END AS decision_dss,

    zona_arbitraje_optima,
    alerta_critica,
    flag_gasto_cero

FROM didi_procesado_v1
ORDER BY fecha;


-- ─── 3. ROI AUDITADO DEL PERÍODO ────────────────────────────────────────────
-- PROTOCOLO: filtro WHERE gastos_operativos > 0 es OBLIGATORIO.
-- Las 6 jornadas con gasto=$0 producen roi_diario=NULL (indefinición matemática).
-- El ROI del período se calcula sobre las utilidades y gastos de N_válido únicamente.

SELECT
    COUNT(*)                                                    AS N_total,
    SUM(CASE WHEN gastos_operativos > 0 THEN 1 ELSE 0 END)     AS N_valido,
    SUM(CASE WHEN gastos_operativos = 0 THEN 1 ELSE 0 END)     AS N_brecha_integridad,
    SUM(garantizado_meta)                                       AS ingreso_bruto_total,
    SUM(gastos_operativos)                                      AS gastos_totales,
    SUM(utilidad_neta)                                          AS utilidad_neta_total,
    -- ROI auditado: solo sobre N_válido (WHERE gastos > 0)
    ROUND(
        SUM(CASE WHEN gastos_operativos > 0 THEN utilidad_neta ELSE 0 END) /
        NULLIF(SUM(CASE WHEN gastos_operativos > 0 THEN gastos_operativos ELSE 0 END), 0) * 100,
        2
    )                                                           AS roi_periodo_auditado,
    -- ROI medio diario (media de los ratios individuales)
    ROUND(AVG(roi_diario), 2)                                  AS roi_medio_diario,
    ROUND(
        SUBSTRING_INDEX(
            GROUP_CONCAT(roi_diario ORDER BY roi_diario SEPARATOR ','),
            ',', CEIL(COUNT(roi_diario)/2)
        ), 2
    )                                                           AS roi_mediano_aproximado
FROM didi_procesado_v1
WHERE roi_diario IS NOT NULL;  -- Equivalente a WHERE gastos_operativos > 0


-- ─── 4. ASIMETRÍA ALGORÍTMICA ───────────────────────────────────────────────

SELECT
    ROUND(SUM(km_google), 2)                                    AS km_reales_total,
    ROUND(SUM(km_didi), 2)                                      AS km_percibidos_total,
    ROUND(SUM(km_fantasma), 2)                                  AS km_fantasma_total,
    ROUND(SUM(km_fantasma) / SUM(km_google) * 100, 2)          AS pct_divergencia,
    ROUND(AVG(ratio_optimizacion), 3)                           AS ro_media,
    -- Mediana RO (MySQL 8.0+)
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ratio_optimizacion)
          OVER (), 3)                                            AS ro_mediana_aprox,
    ROUND(MIN(ratio_optimizacion), 3)                           AS ro_min,
    ROUND(MAX(ratio_optimizacion), 3)                           AS ro_max,
    ROUND(STDDEV(ratio_optimizacion), 3)                        AS ro_desv_est
FROM didi_procesado_v1;


-- ─── 5. ANÁLISIS POR ZONA RO (Tabla de cuartiles operativos) ────────────────

SELECT
    CASE
        WHEN ratio_optimizacion < 1.30               THEN '1. Sub-activado (<1.30)'
        WHEN ratio_optimizacion BETWEEN 1.30 AND 1.7299 THEN '2. Neutra-Baja (1.30–1.72)'
        WHEN ratio_optimizacion BETWEEN 1.73 AND 1.84   THEN '3. Óptimo (1.73–1.84) ✅'
        WHEN ratio_optimizacion BETWEEN 1.8401 AND 1.9999 THEN '4. Alta (1.85–1.99)'
        WHEN ratio_optimizacion >= 2.0               THEN '5. Crítica (≥2.0) 🔴'
    END                                                         AS zona,
    COUNT(*)                                                    AS N,
    ROUND(AVG(utilidad_neta), 0)                               AS utilidad_neta_media,
    ROUND(AVG(eficiencia_cumplimiento) * 100, 1)               AS eficiencia_media_pct,
    ROUND(AVG(ratio_optimizacion), 3)                          AS ro_promedio,
    ROUND(AVG(pedidos_fisicos), 1)                             AS pedidos_promedio,
    ROUND(SUM(complemento_bono) / SUM(garantizado_meta) * 100, 1) AS prop_bono_pct
FROM didi_procesado_v1
GROUP BY zona
ORDER BY zona;


-- ─── 6. ANÁLISIS POR FRANJA HORARIA ─────────────────────────────────────────

SELECT
    CASE
        WHEN HOUR(STR_TO_DATE(h_inicio, '%H:%i')) BETWEEN 17 AND 20 THEN 'PICO [17:00–20:59]'
        ELSE 'VALLE [otros horarios]'
    END                                                         AS franja,
    COUNT(*)                                                    AS N,
    ROUND(AVG(utilidad_neta), 0)                               AS utilidad_media,
    ROUND(AVG(pedidos_fisicos), 1)                             AS pedidos_promedio,
    ROUND(AVG(utilidad_por_hora), 0)                           AS cop_por_hora_media,
    ROUND(AVG(ratio_optimizacion), 3)                          AS ro_medio
FROM didi_procesado_v1
GROUP BY franja
ORDER BY franja DESC;


-- ─── 7. MODELO PRESCRIPTIVO — UTILIDAD ESPERADA POR PEDIDOS ─────────────────
-- Calcula la utilidad esperada para N pedidos usando β=$14,940 COP/pedido
-- con ajuste de eficiencia para RO ≥ 2.0 (factor=0.973)

SELECT
    p.pedidos_proyectados,
    ROUND(14940 * p.pedidos_proyectados - 54378, 0)            AS utilidad_esperada_base,
    ROUND((14940 * p.pedidos_proyectados - 54378) * 0.973, 0)  AS utilidad_ajustada_ro_critico,
    ROUND(14940 * p.pedidos_proyectados - 54378 + 51320, 0)    AS limite_superior_ic90,
    ROUND(14940 * p.pedidos_proyectados - 54378 - 51320, 0)    AS limite_inferior_ic90
FROM (
    SELECT 5  AS pedidos_proyectados UNION ALL
    SELECT 8  UNION ALL
    SELECT 10 UNION ALL
    SELECT 13 UNION ALL
    SELECT 15 UNION ALL
    SELECT 18 UNION ALL
    SELECT 20
) p
ORDER BY p.pedidos_proyectados;


-- ─── 8. ANÁLISIS DE SENSIBILIDAD — ESCENARIOS RO ────────────────────────────

SELECT
    escenario,
    ro_factor,
    ROUND(2109960 * ro_factor, 0)                              AS ingreso_arbitraje_proyectado,
    ROUND((2299070 + 2109960 * ro_factor - 399500) /
          NULLIF(399500, 0) * 100, 2)                         AS roi_proyectado_pct,
    CASE
        WHEN ro_factor >= 1.0                                  THEN '✅ Viable'
        WHEN ro_factor >= 0.70                                 THEN '⚠️ Umbral crítico'
        ELSE '❌ Inviable'
    END                                                         AS viabilidad
FROM (
    SELECT 'Estado Actual (1.706x)'       AS escenario, 1.000  AS ro_factor UNION ALL
    SELECT 'Reducción -10% (1.536x)',                   0.817  UNION ALL
    SELECT 'Reducción -20% (1.365x)',                   0.576  UNION ALL
    SELECT 'Reducción -30% (1.194x)',                   0.305  UNION ALL
    SELECT 'Convergencia Total (1.000x)',               0.000
) scenarios;


-- ─── 9. DETECCIÓN DE ANOMALÍAS — JORNADAS FUERA DE UMBRAL ───────────────────

SELECT
    fecha,
    h_inicio,
    ROUND(ratio_optimizacion, 3)                               AS ro,
    ROUND(eficiencia_cumplimiento, 3)                          AS eficiencia,
    utilidad_neta,
    flag_gasto_cero,
    CASE
        WHEN ratio_optimizacion >= 2.0                         THEN '🔴 ALERTA: RO Crítico'
        WHEN ratio_optimizacion < 1.30                         THEN '⚠️ Sub-activación algorítmica'
        WHEN eficiencia_cumplimiento < 0.60                    THEN '⚠️ Eficiencia por debajo del 60%'
        WHEN flag_gasto_cero = 1                               THEN '📋 Brecha de Integridad (gasto=$0)'
        ELSE 'Normal'
    END                                                         AS alerta_diagnostica
FROM didi_procesado_v1
WHERE
    ratio_optimizacion >= 2.0
    OR ratio_optimizacion < 1.30
    OR eficiencia_cumplimiento < 0.60
    OR flag_gasto_cero = 1
ORDER BY fecha;


-- ─── 10. QUERY DE RECALIBRACIÓN N+1 ─────────────────────────────────────────
-- Ejecutar después de insertar cada nueva jornada operativa.
-- Recalibra los invariantes del período con la muestra ampliada.

SELECT
    'INVARIANTES RECALIBRADOS'                                  AS tipo,
    COUNT(*)                                                    AS N_total,
    SUM(CASE WHEN gastos_operativos > 0 THEN 1 ELSE 0 END)     AS N_valido_roi,
    ROUND(AVG(ratio_optimizacion), 3)                          AS ro_media_recalibrada,
    ROUND(PERCENTILE_CONT(0.5)
          WITHIN GROUP (ORDER BY ratio_optimizacion) OVER (),
          3)                                                    AS ro_mediana_recalibrada,
    ROUND(
        SUM(CASE WHEN gastos_operativos > 0 THEN utilidad_neta ELSE 0 END) /
        NULLIF(SUM(CASE WHEN gastos_operativos > 0 THEN gastos_operativos ELSE NULL END), 0) * 100,
        2
    )                                                           AS roi_recalibrado_pct,
    NOW()                                                       AS timestamp_recalibracion
FROM didi_procesado_v1
LIMIT 1;

-- ============================================================================
-- FIN queries_auditoria.sql · DSS v1.2 · Principio: Transparencia Radical
-- ============================================================================
