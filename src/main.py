"""
================================================================================
PIPELINE ETL v1.2 — AUDITORÍA DE INTEGRIDAD ALGORÍTMICA
Sistema de Soporte a la Decisión · DiDi Food · San Cristóbal Sur, Bogotá D.C.
================================================================================
Fuente de verdad:   data/raw/didi_analisis_12_01.csv
Salida auditada:    data/processed/didi_procesado_v1.1.csv  (N × 28 variables)
Invariantes:        ROI=782.24% · RO_media=1.706x · β=$14,940 COP/pedido
Versión:            1.2 · Publicado 2026-02-18
================================================================================
PROTOCOLO DE RECALIBRACIÓN (N+1):
  Cada nueva jornada operativa debe agregarse a data/raw/didi_analisis_12_01.csv
  como una fila adicional con el esquema:
    fecha,h_inicio,h_fin,km_google_maps,km_didi_app,ingreso_bruto,
    pedidos_cohete,pedidos_normales,gasto_extra
  Al ejecutar `python src/main.py`, el pipeline recalibra automáticamente
  todos los invariantes matemáticos con la muestra ampliada.
================================================================================
"""

import pandas as pd
import numpy as np
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES DEL MODELO PRESCRIPTIVO (Invariantes v1.2)
# Fuente: Regresión OLS sobre N=26 · pedidos_fisicos → utilidad_neta
# ─────────────────────────────────────────────────────────────────────────────
BETA_PEDIDO         = 14_940        # COP por pedido adicional (coef. de regresión)
SIGMA_RESIDUAL      = 51_320        # Error estándar del modelo (COP)
INTERCEPTO          = -54_378       # Intercepto del modelo OLS
FACTOR_EFIC_CRITICA = 0.973         # Ajuste cuando RO ≥ 2.0

# Umbrales del DSS (sincronizados con app_copiloto.py y queries_auditoria.sql)
RO_OPTIMO_MIN  = 1.73
RO_OPTIMO_MAX  = 1.84
RO_CRITICO     = 2.00
PICO_INICIO    = 17
PICO_FIN       = 21   # Exclusivo: [17:00, 21:00)

# Rutas
BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH       = os.path.join(BASE_DIR, 'data', 'raw', 'didi_analisis_12_01.csv')
PROCESSED_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'didi_procesado_v1.1.csv')


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 1: INGESTA Y VALIDACIÓN
# ─────────────────────────────────────────────────────────────────────────────

def cargar_datos_crudos(path: str) -> pd.DataFrame:
    """Carga el CSV crudo y valida el esquema mínimo de 9 columnas primarias."""
    esquema_requerido = {
        'fecha', 'h_inicio', 'h_fin',
        'km_google_maps', 'km_didi_app', 'ingreso_bruto',
        'pedidos_cohete', 'pedidos_normales', 'gasto_extra'
    }
    df = pd.read_csv(path, dtype={
        'h_inicio': str,
        'h_fin': str,
        'fecha': str
    })
    faltantes = esquema_requerido - set(df.columns)
    if faltantes:
        raise ValueError(f"[ETL ERROR] Columnas faltantes en raw CSV: {faltantes}")
    print(f"  ✓ Dataset cargado: {len(df)} observaciones")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 2: DIMENSIÓN 1 — TIEMPO E IDENTIFICACIÓN
# ─────────────────────────────────────────────────────────────────────────────

def _tiempo_a_minutos(t: str) -> int:
    """Convierte string HH:MM a minutos desde medianoche. Preserva formato string."""
    t = str(t).strip().zfill(5)  # Normaliza '0:12' → '00:12'
    partes = t.split(':')
    return int(partes[0]) * 60 + int(partes[1])


def calcular_duracion_turno(h_inicio: str, h_fin: str) -> float:
    """
    Calcula duración en horas con tratamiento de cruce de medianoche.
    Si h_fin < h_inicio → la jornada cruzó las 00:00 → suma 1440 min.
    """
    min_inicio = _tiempo_a_minutos(h_inicio)
    min_fin    = _tiempo_a_minutos(h_fin)
    if min_fin < min_inicio:
        min_fin += 1440   # Cruce de medianoche
    return round((min_fin - min_inicio) / 60, 2)


def calcular_franja_pico(h_inicio: str) -> int:
    """
    Feature Engineering: PICO = 1 si 17:00 ≤ h_inicio < 21:00 (estricto).
    Ventana de 4 horas exactas · Cualquier inicio fuera → VALLE = 0.
    """
    hora = int(str(h_inicio).strip().split(':')[0])
    return 1 if PICO_INICIO <= hora < PICO_FIN else 0


def procesar_dimension_tiempo(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica transformaciones de tiempo e identidad."""
    df = df.rename(columns={
        'km_google_maps': 'km_google',
        'km_didi_app':    'km_didi',
        'gasto_extra':    'gastos_operativos'
    })
    # Normalizar strings de tiempo
    df['h_inicio'] = df['h_inicio'].astype(str).str.strip().str.zfill(5)
    df['h_fin']    = df['h_fin'].astype(str).str.strip().str.zfill(5)
    # Duración con tratamiento de medianoche
    df['duracion_horas'] = df.apply(
        lambda r: calcular_duracion_turno(r['h_inicio'], r['h_fin']), axis=1
    )
    # Feature: franja horaria
    df['franja_pico'] = df['h_inicio'].apply(calcular_franja_pico)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 3: DIMENSIÓN 2 — DISTANCIA Y RATIO DE OPTIMIZACIÓN
# ─────────────────────────────────────────────────────────────────────────────

def procesar_dimension_distancia(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula km_fantasma y ratio_optimizacion (RO).
    RO = km_didi / km_google → Métrica central de asimetría algorítmica.
    """
    df['km_fantasma']          = (df['km_didi'] - df['km_google']).round(2)
    df['ratio_optimizacion']   = (df['km_didi'] / df['km_google']).round(4)
    return df


def calcular_features_ro(df: pd.DataFrame) -> pd.DataFrame:
    """
    Feature Engineering DSS basado en ratio_optimizacion:
      - zona_arbitraje_optima: 1 si 1.73 ≤ RO ≤ 1.84
      - alerta_critica:        1 si RO ≥ 2.0
    Mutuamente excluyentes por construcción (rango óptimo ∩ crítico = ∅).
    """
    ro = df['ratio_optimizacion']
    df['zona_arbitraje_optima'] = ((ro >= RO_OPTIMO_MIN) & (ro <= RO_OPTIMO_MAX)).astype(int)
    df['alerta_critica']        = (ro >= RO_CRITICO).astype(int)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 4: DIMENSIÓN 3 — INGRESO (SEPARACIÓN MECE)
# ─────────────────────────────────────────────────────────────────────────────

def separar_ingreso_mece(df: pd.DataFrame) -> pd.DataFrame:
    """
    Separa ingreso_bruto en sus dos componentes MECE:
      ingreso_base      (Ingreso-Trabajo):     52.1% del bruto
      complemento_bono  (Ingreso-Arbitraje):   47.9% del bruto
    
    NOTA METODOLÓGICA: La proporción 52.1%/47.9% es el invariante auditado
    del período N=26. Para ciclos N+1 con datos individuales disponibles,
    sustituir por los valores reales de cada jornada.
    La suma ingreso_base + complemento_bono = garantizado_meta (= ingreso_bruto)
    preserva exhaustividad colectiva del principio MECE.
    """
    PROP_BASE = 0.521
    df['ingreso_base']      = (df['ingreso_bruto'] * PROP_BASE).round(0).astype(int)
    df['complemento_bono']  = df['ingreso_bruto'] - df['ingreso_base']
    df['garantizado_meta']  = df['ingreso_bruto']   # Alias semántico · igualdad exacta
    df['proporcion_bono']   = (df['complemento_bono'] / df['garantizado_meta']).round(4)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 5: DIMENSIÓN 4 — COSTO E INTEGRIDAD
# ─────────────────────────────────────────────────────────────────────────────

def procesar_dimension_costo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Documenta las 6 jornadas con gastos_operativos = 0.
    Protocolo de Transparencia Radical: preservar como NaN en roi_diario,
    NO imputar, NO eliminar del dataset.
    """
    df['gastos_operativos'] = df['gastos_operativos'].fillna(0).astype(int)
    df['flag_gasto_cero']   = (df['gastos_operativos'] == 0).astype(int)
    n_gasto_cero = df['flag_gasto_cero'].sum()
    if n_gasto_cero > 0:
        print(f"  ⚠  Brecha de Integridad: {n_gasto_cero} jornadas con gastos_operativos=$0 "
              f"→ roi_diario=NaN (preservados, no imputados)")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 6: DIMENSIÓN 5 — RESULTADO
# ─────────────────────────────────────────────────────────────────────────────

def calcular_resultados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula métricas de resultado:
      utilidad_neta      = garantizado_meta - gastos_operativos
      utilidad_por_hora  = utilidad_neta / duracion_horas
      roi_diario         = (utilidad_neta / gastos_operativos) × 100
                           NaN cuando gastos_operativos = 0 (indefinición matemática)
      rentabilidad_binaria = 1 si utilidad_neta > 0
    """
    df['utilidad_neta']       = df['garantizado_meta'] - df['gastos_operativos']
    df['utilidad_por_hora']   = (df['utilidad_neta'] / df['duracion_horas']).round(2)
    df['roi_diario']          = np.where(
        df['gastos_operativos'] > 0,
        (df['utilidad_neta'] / df['gastos_operativos'] * 100).round(2),
        np.nan
    )
    df['rentabilidad_binaria'] = (df['utilidad_neta'] > 0).astype(int)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 7: DIMENSIÓN 6 — PRODUCCIÓN Y EFICIENCIA
# ─────────────────────────────────────────────────────────────────────────────

def procesar_dimension_produccion(df: pd.DataFrame) -> pd.DataFrame:
    """
    pedidos_fisicos    = pedidos_cohete + pedidos_normales
    unidades_progreso  = pedidos_cohete  (contabilización DiDi para meta de bono)
    eficiencia_cumplimiento = unidades_progreso / pedidos_fisicos
    """
    df['pedidos_fisicos']          = df['pedidos_cohete'] + df['pedidos_normales']
    df['unidades_progreso']        = df['pedidos_cohete']
    df['eficiencia_cumplimiento']  = (
        df['unidades_progreso'] / df['pedidos_fisicos']
    ).round(4)
    df['km_por_pedido_google']     = (df['km_google'] / df['pedidos_fisicos']).round(4)
    df['km_por_pedido_didi']       = (df['km_didi']   / df['pedidos_fisicos']).round(4)
    df['ingreso_por_km_google']    = (df['garantizado_meta'] / df['km_google']).round(2)
    df['ingreso_por_hora']         = (df['garantizado_meta'] / df['duracion_horas']).round(2)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 8: CÁLCULO DE INVARIANTES Y AUDITORÍA
# ─────────────────────────────────────────────────────────────────────────────

def calcular_invariantes(df: pd.DataFrame) -> dict:
    """
    Recalibra los invariantes matemáticos del período completo.
    Permite recalibración automática ante cada N+1.
    """
    inv = {}
    inv['N_total']        = len(df)
    inv['N_valido_roi']   = df['flag_gasto_cero'].eq(0).sum()

    # Métricas financieras auditadas
    inv['ingreso_bruto_total']  = int(df['garantizado_meta'].sum())
    inv['gastos_totales']       = int(df['gastos_operativos'].sum())
    inv['utilidad_neta_total']  = int(df['utilidad_neta'].sum())

    # ROI del período (N válido)
    gastos_validos = df.loc[df['flag_gasto_cero'] == 0, 'gastos_operativos'].sum()
    util_valida    = df.loc[df['flag_gasto_cero'] == 0, 'utilidad_neta'].sum()
    inv['roi_periodo'] = round((util_valida / gastos_validos) * 100, 2)

    # Asimetría algorítmica
    inv['km_google_total'] = round(df['km_google'].sum(), 2)
    inv['km_didi_total']   = round(df['km_didi'].sum(), 2)
    inv['km_fantasma_total'] = round(inv['km_didi_total'] - inv['km_google_total'], 2)
    inv['ro_media']   = round(df['ratio_optimizacion'].mean(), 3)
    inv['ro_mediana'] = round(df['ratio_optimizacion'].median(), 3)

    # IC 95% para RO (t-Student)
    ro_vals = df['ratio_optimizacion'].dropna()
    t_ci = stats.t.interval(0.95, df=len(ro_vals)-1,
                             loc=ro_vals.mean(), scale=stats.sem(ro_vals))
    inv['ro_ic95_lo'] = round(t_ci[0], 3)
    inv['ro_ic95_hi'] = round(t_ci[1], 3)

    # Regresión: pedidos_fisicos → utilidad_neta
    slope, intercept, r_val, p_val, se = stats.linregress(
        df['pedidos_fisicos'], df['utilidad_neta']
    )
    inv['beta_pedido']  = round(slope, 2)
    inv['intercepto']   = round(intercept, 2)
    inv['r_pearson']    = round(r_val, 3)
    inv['r_squared']    = round(r_val**2, 3)
    inv['p_value']      = round(p_val, 6)

    # Sigma residual
    y_pred   = slope * df['pedidos_fisicos'] + intercept
    residuos = df['utilidad_neta'] - y_pred
    inv['sigma_residual'] = round(residuos.std(), 2)

    return inv


def imprimir_reporte(inv: dict):
    """Imprime el reporte de auditoría al stdout."""
    sep = "=" * 70
    print(f"\n{sep}")
    print("PIPELINE ETL v1.2 — AUDITORÍA DE INTEGRIDAD ALGORÍTMICA")
    print(sep)
    print(f"  N Total:              {inv['N_total']} jornadas")
    print(f"  N Válido (ROI):       {inv['N_valido_roi']} jornadas")
    print(f"  Brecha Integridad:    {inv['N_total'] - inv['N_valido_roi']} jornadas (gastos=$0 → NaN)")
    print()
    print(f"  ── MÉTRICAS FINANCIERAS ──────────────────────────────")
    print(f"  Ingreso Bruto Total:  ${inv['ingreso_bruto_total']:,} COP")
    print(f"  Gastos Totales:       ${inv['gastos_totales']:,} COP")
    print(f"  Utilidad Neta Total:  ${inv['utilidad_neta_total']:,} COP")
    print(f"  ROI del Período:      {inv['roi_periodo']}%   [AUDITADO · N={inv['N_valido_roi']}]")
    print()
    print(f"  ── ASIMETRÍA ALGORÍTMICA ────────────────────────────")
    print(f"  km Google Maps:       {inv['km_google_total']:,} km")
    print(f"  km DiDi App:          {inv['km_didi_total']:,} km")
    print(f"  km Fantasma:          {inv['km_fantasma_total']:,} km")
    print(f"  RO Media:             {inv['ro_media']}x")
    print(f"  RO Mediana:           {inv['ro_mediana']}x")
    print(f"  RO IC 95%:            [{inv['ro_ic95_lo']}, {inv['ro_ic95_hi']}]")
    print()
    print(f"  ── MODELO PRESCRIPTIVO ──────────────────────────────")
    print(f"  β (pedidos→utilidad): ${inv['beta_pedido']:,} COP/pedido")
    print(f"  Intercepto:           ${inv['intercepto']:,} COP")
    print(f"  r de Pearson:         {inv['r_pearson']}    p={inv['p_value']}")
    print(f"  R²:                   {inv['r_squared']} ({inv['r_squared']*100:.1f}% varianza explicada)")
    print(f"  σ residual:           ${inv['sigma_residual']:,} COP")
    print()
    print(f"  Feature Engineering:  franja_pico | zona_arbitraje_optima | alerta_critica ✅")
    print(f"{sep}")
    print(f"  ✅ PIPELINE v1.2 COMPLETADO — 28 columnas exportadas")
    print(f"{sep}\n")


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 9: ORDENAMIENTO Y EXPORTACIÓN
# ─────────────────────────────────────────────────────────────────────────────

ORDEN_COLUMNAS_28 = [
    # Dimensión 1: Tiempo-Identificación (5)
    'fecha', 'h_inicio', 'h_fin', 'duracion_horas', 'franja_pico',
    # Dimensión 2: Distancia (4)
    'km_google', 'km_didi', 'km_fantasma', 'ratio_optimizacion',
    # Dimensión 3: Ingreso MECE (4)
    'ingreso_base', 'complemento_bono', 'garantizado_meta', 'proporcion_bono',
    # Dimensión 4: Costo e Integridad (2)
    'gastos_operativos', 'flag_gasto_cero',
    # Dimensión 5: Resultado (4)
    'utilidad_neta', 'utilidad_por_hora', 'roi_diario', 'rentabilidad_binaria',
    # Dimensión 6: Producción y Eficiencia (7)
    'pedidos_fisicos', 'unidades_progreso', 'eficiencia_cumplimiento',
    'km_por_pedido_google', 'km_por_pedido_didi',
    'ingreso_por_km_google', 'ingreso_por_hora',
    # Dimensión 7: Feature Engineering DSS (3) — ya incluido: franja_pico arriba
    'zona_arbitraje_optima', 'alerta_critica'
]


def exportar_procesado(df: pd.DataFrame, path: str):
    """Exporta el dataset procesado con las 28 columnas MECE en orden canónico."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # franja_pico ya está en Dimensión 1 → no duplicar en Dimensión 7
    cols_disponibles = [c for c in ORDEN_COLUMNAS_28 if c in df.columns]
    df_out = df[cols_disponibles].copy()
    df_out.to_csv(path, index=False, float_format='%.4f')
    print(f"  ✓ Dataset procesado exportado: {path}")
    print(f"    Dimensiones: {df_out.shape[0]} filas × {df_out.shape[1]} columnas")
    return df_out


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def ejecutar_pipeline(raw_path: str = RAW_PATH,
                      processed_path: str = PROCESSED_PATH) -> pd.DataFrame:
    """
    Ejecuta el pipeline completo ETL v1.2.
    Retorna el DataFrame procesado con 28 variables MECE.
    Recalibra todos los invariantes automáticamente ante N+1.
    """
    print("\n🔄 Iniciando Pipeline ETL v1.2...")

    df = cargar_datos_crudos(raw_path)
    df = procesar_dimension_tiempo(df)
    df = procesar_dimension_distancia(df)
    df = separar_ingreso_mece(df)
    df = procesar_dimension_costo(df)
    df = calcular_resultados(df)
    df = procesar_dimension_produccion(df)
    df = calcular_features_ro(df)

    inv    = calcular_invariantes(df)
    df_out = exportar_procesado(df, processed_path)
    imprimir_reporte(inv)

    return df_out


if __name__ == '__main__':
    ejecutar_pipeline()
