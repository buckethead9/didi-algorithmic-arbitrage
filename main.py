#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline de Auditoría de Arbitraje Algorítmico - DiDi Food
Autor: Ingeniero de Datos Senior
Versión: 1.0.0
Python: 3.14+

Propósito: Procesamiento y normalización de datos operativos de DiDi Food
para análisis de asimetría algorítmica entre rutas Google Maps y DiDi App.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import re

# ====================================================================
# CONFIGURACIÓN DE RUTAS (Manejo MAX_PATH para Windows)
# ====================================================================

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent.resolve()
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

# Crear directorios si no existen
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Rutas de archivos
INPUT_FILE = RAW_DATA_DIR / "didi_analisis_12_01.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "didi_procesado.csv"


# ====================================================================
# FUNCIONES DE LIMPIEZA Y TRANSFORMACIÓN
# ====================================================================

def limpiar_kilometros(valor_km: str) -> float:
    """
    Normaliza strings de kilómetros a float.
    
    Transforma "45,06 km" → 45.06
    
    Args:
        valor_km: String con formato "X,XX km" o variantes
        
    Returns:
        float: Valor numérico limpio
    """
    if pd.isna(valor_km):
        return 0.0
    
    # Convertir a string y limpiar
    valor_str = str(valor_km).strip()
    
    # Remover " km" y espacios
    valor_str = valor_str.replace(" km", "").replace("km", "").strip()
    
    # Reemplazar coma por punto (formato decimal colombiano)
    valor_str = valor_str.replace(",", ".")
    
    try:
        return float(valor_str)
    except ValueError:
        print(f"⚠️  Advertencia: No se pudo convertir '{valor_km}' a float. Retornando 0.0")
        return 0.0


def calcular_duracion_turno(hora_inicio: str, hora_fin: str) -> float:
    """
    Calcula la duración del turno en horas, manejando cruces de medianoche.
    
    TRATAMIENTO DE MEDIANOCHE (Día Operativo):
    Si hora_fin < hora_inicio, el turno cruzó la medianoche.
    Se suma 24 horas a hora_fin para obtener la duración correcta.
    
    Ejemplos:
        - 17:01 a 23:23 → 6.37 horas
        - 17:01 a 0:12 → 7.18 horas (cruce de medianoche)
        - 12:44 a 0:02 → 11.30 horas (cruce de medianoche)
    
    Args:
        hora_inicio: String en formato "HH:MM"
        hora_fin: String en formato "HH:MM"
        
    Returns:
        float: Duración en horas con 2 decimales
    """
    def parse_hora(hora_str: str) -> tuple:
        """Extrae horas y minutos de string HH:MM"""
        h, m = map(int, hora_str.strip().split(":"))
        return h, m
    
    h_ini, m_ini = parse_hora(hora_inicio)
    h_fin, m_fin = parse_hora(hora_fin)
    
    # Convertir a minutos totales
    minutos_inicio = h_ini * 60 + m_ini
    minutos_fin = h_fin * 60 + m_fin
    
    # Detectar cruce de medianoche
    if minutos_fin < minutos_inicio:
        # Sumar 24 horas (1440 minutos) a la hora de fin
        minutos_fin += 1440
    
    # Calcular duración en minutos
    duracion_minutos = minutos_fin - minutos_inicio
    
    # Convertir a horas
    duracion_horas = duracion_minutos / 60.0
    
    return round(duracion_horas, 2)


def calcular_metricas_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula todas las métricas derivadas del dataset.
    
    Variables Derivadas (13):
    - duracion_horas: Duración del turno con manejo de medianoche
    - utilidad_neta: garantizado_meta - gastos_operativos
    - km_por_pedido_google: km_google / pedidos_fisicos
    - km_por_pedido_didi: km_didi / pedidos_fisicos
    - ratio_optimizacion (RO): km_didi / km_google
    - ingreso_por_km_google: garantizado_meta / km_google
    - ingreso_por_km_didi: garantizado_meta / km_didi
    - ingreso_por_hora: garantizado_meta / duracion_horas
    - utilidad_por_hora: utilidad_neta / duracion_horas
    - eficiencia_cumplimiento: unidades_progreso / pedidos_fisicos
    - proporcion_bono: complemento_bono / garantizado_meta
    - roi_diario: (utilidad_neta / gastos_operativos) * 100 si gastos > 0
    - rentabilidad_binaria: 1 si utilidad_neta > 0, 0 si no
    
    Args:
        df: DataFrame con datos limpios
        
    Returns:
        DataFrame con columnas derivadas agregadas
    """
    df_metricas = df.copy()
    
    # 1. Duración del turno
    df_metricas['duracion_horas'] = df_metricas.apply(
        lambda row: calcular_duracion_turno(row['h_inicio'], row['h_fin']),
        axis=1
    )
    
    # 2. Utilidad Neta (COP)
    df_metricas['utilidad_neta'] = df_metricas['garantizado_meta'] - df_metricas['gastos_operativos']
    
    # 3. KM por pedido
    df_metricas['km_por_pedido_google'] = np.where(
        df_metricas['pedidos_fisicos'] > 0,
        df_metricas['km_google'] / df_metricas['pedidos_fisicos'],
        0
    )
    df_metricas['km_por_pedido_didi'] = np.where(
        df_metricas['pedidos_fisicos'] > 0,
        df_metricas['km_didi'] / df_metricas['pedidos_fisicos'],
        0
    )
    
    # 4. Ratio de Optimización (RO) - Eficiencia de Distancia
    df_metricas['ratio_optimizacion'] = np.where(
        df_metricas['km_google'] > 0,
        df_metricas['km_didi'] / df_metricas['km_google'],
        0
    )
    
    # 5. Ingreso por KM
    df_metricas['ingreso_por_km_google'] = np.where(
        df_metricas['km_google'] > 0,
        df_metricas['garantizado_meta'] / df_metricas['km_google'],
        0
    )
    df_metricas['ingreso_por_km_didi'] = np.where(
        df_metricas['km_didi'] > 0,
        df_metricas['garantizado_meta'] / df_metricas['km_didi'],
        0
    )
    
    # 6. Ingreso por hora
    df_metricas['ingreso_por_hora'] = np.where(
        df_metricas['duracion_horas'] > 0,
        df_metricas['garantizado_meta'] / df_metricas['duracion_horas'],
        0
    )
    
    # 7. Utilidad por hora
    df_metricas['utilidad_por_hora'] = np.where(
        df_metricas['duracion_horas'] > 0,
        df_metricas['utilidad_neta'] / df_metricas['duracion_horas'],
        0
    )
    
    # 8. Eficiencia de cumplimiento
    df_metricas['eficiencia_cumplimiento'] = np.where(
        df_metricas['pedidos_fisicos'] > 0,
        df_metricas['unidades_progreso'] / df_metricas['pedidos_fisicos'],
        0
    )
    
    # 9. Proporción de bono
    df_metricas['proporcion_bono'] = np.where(
        df_metricas['garantizado_meta'] > 0,
        df_metricas['complemento_bono'] / df_metricas['garantizado_meta'],
        0
    )
    
    # 10. ROI Diario (solo si hay gastos)
    df_metricas['roi_diario'] = np.where(
        df_metricas['gastos_operativos'] > 0,
        (df_metricas['utilidad_neta'] / df_metricas['gastos_operativos']) * 100,
        np.nan  # No calculable si no hay gastos
    )
    
    # 11. Rentabilidad binaria (indicador de éxito)
    df_metricas['rentabilidad_binaria'] = np.where(
        df_metricas['utilidad_neta'] > 0,
        1,
        0
    )
    
    # Redondear métricas a 2 decimales
    columnas_redondeo = [
        'duracion_horas', 'km_por_pedido_google', 'km_por_pedido_didi',
        'ratio_optimizacion', 'ingreso_por_km_google', 'ingreso_por_km_didi',
        'ingreso_por_hora', 'utilidad_por_hora', 'eficiencia_cumplimiento',
        'proporcion_bono', 'roi_diario'
    ]
    
    for col in columnas_redondeo:
        if col in df_metricas.columns:
            df_metricas[col] = df_metricas[col].round(2)
    
    return df_metricas


def generar_reporte_auditoria(df: pd.DataFrame) -> dict:
    """
    Genera métricas de auditoría global del pipeline.
    
    Métricas Globales (Transparencia Radical):
    - N: Número de registros
    - Total Ingresos (COP)
    - Total Gastos (COP)
    - Utilidad Neta (COP)
    - ROI Global (%)
    - RO Global (Ratio de Optimización)
    - Múltiplo de Ingreso (Ingresos/Gastos)
    - Días con Gasto Cero (anomalía)
    - Turnos con Cruce de Medianoche
    
    Args:
        df: DataFrame procesado
        
    Returns:
        dict: Diccionario con métricas de auditoría
    """
    # Filtrar solo registros con gastos > 0 para ROI
    df_con_gastos = df[df['gastos_operativos'] > 0]
    
    # Detectar cruces de medianoche
    def detectar_medianoche(row):
        h_ini = int(row['h_inicio'].split(':')[0])
        h_fin = int(row['h_fin'].split(':')[0])
        return 1 if h_fin < h_ini else 0
    
    turnos_medianoche = df.apply(detectar_medianoche, axis=1).sum()
    
    reporte = {
        'n_registros': len(df),
        'total_ingresos_cop': df['garantizado_meta'].sum(),
        'total_gastos_cop': df['gastos_operativos'].sum(),
        'utilidad_neta_cop': df['utilidad_neta'].sum(),
        'roi_global_pct': None,
        'ro_global': df['ratio_optimizacion'].mean(),
        'multiplo_ingreso': None,
        'dias_gasto_cero': len(df[df['gastos_operativos'] == 0]),
        'turnos_cruce_medianoche': turnos_medianoche,
        'km_google_total': df['km_google'].sum(),
        'km_didi_total': df['km_didi'].sum(),
        'pedidos_total': df['pedidos_fisicos'].sum(),
        'duracion_total_horas': df['duracion_horas'].sum()
    }
    
    # Calcular ROI Global (solo sobre gastos reales)
    if reporte['total_gastos_cop'] > 0:
        reporte['roi_global_pct'] = (reporte['utilidad_neta_cop'] / reporte['total_gastos_cop']) * 100
        reporte['multiplo_ingreso'] = reporte['total_ingresos_cop'] / reporte['total_gastos_cop']
    else:
        reporte['roi_global_pct'] = np.nan
        reporte['multiplo_ingreso'] = np.nan
    
    # Redondear métricas
    reporte['roi_global_pct'] = round(reporte['roi_global_pct'], 2)
    reporte['ro_global'] = round(reporte['ro_global'], 2)
    reporte['multiplo_ingreso'] = round(reporte['multiplo_ingreso'], 2)
    
    return reporte


# ====================================================================
# PIPELINE PRINCIPAL
# ====================================================================

def main():
    """
    Pipeline de ejecución principal.
    
    Flujo:
    1. Carga de datos raw
    2. Limpieza de kilómetros
    3. Cálculo de métricas derivadas
    4. Generación de reporte de auditoría
    5. Exportación a CSV procesado
    """
    print("=" * 70)
    print("PIPELINE DE AUDITORÍA - ARBITRAJE ALGORÍTMICO DIDI FOOD")
    print("=" * 70)
    print(f"\n📂 Directorio Base: {BASE_DIR}")
    print(f"📥 Archivo Entrada: {INPUT_FILE}")
    print(f"📤 Archivo Salida: {OUTPUT_FILE}\n")
    
    # ----------------------------------------------------------------
    # PASO 1: CARGA DE DATOS
    # ----------------------------------------------------------------
    print("🔄 [PASO 1/5] Cargando datos raw...")
    
    if not INPUT_FILE.exists():
        print(f"❌ ERROR: No se encontró el archivo {INPUT_FILE}")
        sys.exit(1)
    
    try:
        df = pd.read_csv(INPUT_FILE, encoding='utf-8')
        print(f"✅ Cargados {len(df)} registros")
    except Exception as e:
        print(f"❌ ERROR al cargar CSV: {e}")
        sys.exit(1)
    
    # ----------------------------------------------------------------
    # PASO 2: LIMPIEZA DE KILÓMETROS
    # ----------------------------------------------------------------
    print("\n🧹 [PASO 2/5] Limpiando valores de kilómetros...")
    
    df['km_google'] = df['km_google_maps'].apply(limpiar_kilometros)
    df['km_didi'] = df['km_didi_app'].apply(limpiar_kilometros)
    
    print(f"✅ Limpieza completada")
    print(f"   - KM Google total: {df['km_google'].sum():.2f} km")
    print(f"   - KM DiDi total: {df['km_didi'].sum():.2f} km")
    
    # ----------------------------------------------------------------
    # PASO 3: CÁLCULO DE MÉTRICAS DERIVADAS
    # ----------------------------------------------------------------
    print("\n📊 [PASO 3/5] Calculando métricas derivadas...")
    
    df = calcular_metricas_derivadas(df)
    
    print(f"✅ Generadas 13 variables derivadas")
    
    # ----------------------------------------------------------------
    # PASO 4: REPORTE DE AUDITORÍA
    # ----------------------------------------------------------------
    print("\n🔍 [PASO 4/5] Generando reporte de auditoría...")
    
    reporte = generar_reporte_auditoria(df)
    
    print("\n" + "=" * 70)
    print("MÉTRICAS GLOBALES DE AUDITORÍA (N={})".format(reporte['n_registros']))
    print("=" * 70)
    print(f"💰 Total Ingresos:        ${reporte['total_ingresos_cop']:,.0f} COP")
    print(f"💸 Total Gastos:          ${reporte['total_gastos_cop']:,.0f} COP")
    print(f"💵 Utilidad Neta:         ${reporte['utilidad_neta_cop']:,.0f} COP")
    print(f"📈 ROI Global:            {reporte['roi_global_pct']:.2f}%")
    print(f"🔢 Múltiplo de Ingreso:   {reporte['multiplo_ingreso']:.2f}x")
    print(f"🛣️  RO Global:             {reporte['ro_global']:.2f}x")
    print(f"📦 Total Pedidos:         {reporte['pedidos_total']}")
    print(f"⏱️  Duración Total:        {reporte['duracion_total_horas']:.2f} horas")
    print("=" * 70)
    print("\n🚨 ANOMALÍAS DETECTADAS:")
    print(f"   - Días con Gasto $0: {reporte['dias_gasto_cero']} (ROI no calculable)")
    print(f"   - Turnos con cruce de medianoche: {reporte['turnos_cruce_medianoche']}")
    print("=" * 70)
    
    # ----------------------------------------------------------------
    # PASO 5: EXPORTACIÓN
    # ----------------------------------------------------------------
    print("\n💾 [PASO 5/5] Exportando datos procesados...")
    
    # Seleccionar columnas finales
    columnas_finales = [
        'fecha', 'h_inicio', 'h_fin', 'duracion_horas',
        'km_google', 'km_didi', 'ratio_optimizacion',
        'pedidos_fisicos', 'unidades_progreso', 'eficiencia_cumplimiento',
        'garantizado_meta', 'ingreso_base', 'complemento_bono', 'proporcion_bono',
        'gastos_operativos', 'utilidad_neta',
        'km_por_pedido_google', 'km_por_pedido_didi',
        'ingreso_por_km_google', 'ingreso_por_km_didi',
        'ingreso_por_hora', 'utilidad_por_hora',
        'roi_diario', 'rentabilidad_binaria'
    ]
    
    df_final = df[columnas_finales].copy()
    
    try:
        df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
        print(f"✅ Archivo exportado exitosamente: {OUTPUT_FILE}")
        print(f"   Tamaño: {OUTPUT_FILE.stat().st_size / 1024:.2f} KB")
    except Exception as e:
        print(f"❌ ERROR al exportar: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print("\n💡 Siguiente paso: Ejecutar ANALISIS_SQL_FINAL.sql en MySQL 8.0")
    print("   o importar didi_procesado.csv a tu herramienta de BI preferida.\n")


if __name__ == "__main__":
    main()
