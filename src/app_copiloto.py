"""
================================================================================
DSS v1.2 — SISTEMA DE SOPORTE A LA DECISIÓN
DiDi Food · Gig Economy · San Cristóbal Sur, Bogotá D.C.
================================================================================
Arquitectura:   Patrón Z · KPIs (área óptica primaria) → Gráfico asimetría
                (centro) → Panel de Decisión Binarizada [SÍ/NO OPERAR] (área terminal)
HOPs:           50 trayectorias de regresión simuladas · β=$14,940 · σ=$51,320
Umbrales:       Óptimo [1.73–1.84] · Crítico [≥2.0]
Ejecución:      streamlit run src/app_copiloto.py
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os, sys

# ─── Importar pipeline ETL ───────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
try:
    from main import ejecutar_pipeline, BETA_PEDIDO, SIGMA_RESIDUAL, INTERCEPTO
    from main import RO_OPTIMO_MIN, RO_OPTIMO_MAX, RO_CRITICO, FACTOR_EFIC_CRITICA
except ImportError:
    # Fallback: constantes inline si se ejecuta standalone
    BETA_PEDIDO         = 14_940
    SIGMA_RESIDUAL      = 51_320
    INTERCEPTO          = -54_378
    RO_OPTIMO_MIN       = 1.73
    RO_OPTIMO_MAX       = 1.84
    RO_CRITICO          = 2.00
    FACTOR_EFIC_CRITICA = 0.973

# ─── Paleta Tufte ────────────────────────────────────────────────────────────
COLOR_GRIS   = '#D3D3D3'
COLOR_VERDE  = '#2ECC71'
COLOR_ROJO   = '#E74C3C'
COLOR_AZUL   = '#3498DB'
COLOR_TEXTO  = '#2C3E50'
BG_DARK      = '#0E1117'

# ─── Configuración de página ─────────────────────────────────────────────────
st.set_page_config(
    page_title="DSS v1.2 — DiDi Soberanía de Datos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .metric-card {
        background: #1A1D2E; border-radius: 8px; padding: 16px;
        border-left: 4px solid #3498DB; margin-bottom: 8px;
    }
    .decision-si {
        background: #0D3B1E; border-radius: 12px; padding: 24px;
        border: 2px solid #2ECC71; text-align: center;
    }
    .decision-no {
        background: #3B0D0D; border-radius: 12px; padding: 24px;
        border: 2px solid #E74C3C; text-align: center;
    }
    .decision-monitor {
        background: #1A1A0D; border-radius: 12px; padding: 24px;
        border: 2px solid #F39C12; text-align: center;
    }
    h1 { color: #ECF0F1 !important; font-size: 1.6rem !important; }
    h2 { color: #BDC3C7 !important; font-size: 1.1rem !important; }
    .stMetric label { color: #95A5A6 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CARGA DE DATOS
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def cargar_datos() -> pd.DataFrame:
    """Carga o regenera el dataset procesado (recalibra en cada ejecución)."""
    processed_path = os.path.join(BASE_DIR, 'data', 'processed', 'didi_procesado_v1.1.csv')
    if not os.path.exists(processed_path):
        try:
            ejecutar_pipeline()
        except Exception:
            pass
    if os.path.exists(processed_path):
        return pd.read_csv(processed_path)
    else:
        st.error("Dataset no encontrado. Ejecuta `python src/main.py` primero.")
        st.stop()

df = cargar_datos()
n_total    = len(df)
n_valido   = int((df['flag_gasto_cero'] == 0).sum())
roi_periodo = round(
    df.loc[df['flag_gasto_cero']==0, 'utilidad_neta'].sum() /
    df.loc[df['flag_gasto_cero']==0, 'gastos_operativos'].sum() * 100, 2
)
ro_media   = round(df['ratio_optimizacion'].mean(), 3)
ro_mediana = round(df['ratio_optimizacion'].median(), 3)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — INGESTA DE VARIABLES (CAPA 4 DSS)
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🎛️ Ingesta DSS — Capa 4")
    st.markdown("*Ingresa las variables de la jornada actual para obtener la decisión binarizada.*")
    st.divider()

    pedidos_input = st.slider(
        "Pedidos físicos proyectados", min_value=1, max_value=25,
        value=13, step=1, help="Cantidad de pedidos que planeas completar en la jornada"
    )
    ro_input = st.number_input(
        "Ratio de Optimización (RO) observado",
        min_value=0.5, max_value=3.5, value=float(ro_media),
        step=0.01, format="%.2f",
        help="RO = km_didi / km_google de jornadas recientes en tu zona"
    )
    hora_inicio = st.selectbox(
        "Hora de inicio proyectada",
        options=[f"{h:02d}:00" for h in range(6, 24)] + ["00:00", "01:00"],
        index=11,
        help="Determina franja PICO [17:00–21:00) vs VALLE"
    )
    n_hops = st.slider(
        "Trayectorias HOPs a simular", min_value=20, max_value=100,
        value=50, step=10,
        help="Hypothetical Outcome Plots: cuántas trayectorias de regresión mostrar"
    )
    st.divider()
    st.markdown("**Umbrales DSS (Invariantes v1.2)**")
    st.markdown(f"- ✅ Óptimo: `{RO_OPTIMO_MIN} ≤ RO ≤ {RO_OPTIMO_MAX}`")
    st.markdown(f"- 🔴 Crítico: `RO ≥ {RO_CRITICO}`")
    st.markdown(f"- ⏰ PICO: `17:00 – 21:00`")
    st.markdown(f"- β = `${BETA_PEDIDO:,} COP/pedido`")

# ─────────────────────────────────────────────────────────────────────────────
# CÁLCULOS DSS
# ─────────────────────────────────────────────────────────────────────────────

hora_int  = int(hora_inicio.split(':')[0])
es_pico   = 17 <= hora_int < 21
zona_opt  = RO_OPTIMO_MIN <= ro_input <= RO_OPTIMO_MAX
alerta    = ro_input >= RO_CRITICO
factor_ef = FACTOR_EFIC_CRITICA if alerta else 1.0

# Utilidad esperada puntual
util_esperada = int(BETA_PEDIDO * pedidos_input + INTERCEPTO)
util_ajustada = int(util_esperada * factor_ef)

# Decisión binarizada
if alerta:
    decision = "🔴 NO OPERAR"
    decision_class = "decision-no"
    razon = f"RO={ro_input:.2f} ≥ {RO_CRITICO} → Eficiencia de cumplimiento colapsará ~7.9%. Cambiar de zona."
elif zona_opt:
    decision = "✅ SÍ OPERAR"
    decision_class = "decision-si"
    razon = f"RO={ro_input:.2f} en zona óptima [{RO_OPTIMO_MIN}–{RO_OPTIMO_MAX}]. Utilidad máxima esperada."
elif ro_input < 1.30:
    decision = "⚠️ EVALUAR VIABILIDAD"
    decision_class = "decision-monitor"
    razon = f"RO={ro_input:.2f} < 1.30 → Sub-activación algorítmica. Bono en riesgo."
else:
    decision = "🟡 MONITOREAR"
    decision_class = "decision-monitor"
    razon = f"RO={ro_input:.2f} fuera de zona óptima. Continuar con vigilancia de RO."

# HOPs: 50 trayectorias de regresión con σ residual
np.random.seed(42)
pedidos_range = np.linspace(1, 25, 50)
hops_matrix   = np.array([
    BETA_PEDIDO * pedidos_range + INTERCEPTO + np.random.normal(0, SIGMA_RESIDUAL, 50)
    for _ in range(n_hops)
])


# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT — PATRÓN Z
# ─────────────────────────────────────────────────────────────────────────────

# ZONA SUPERIOR: KPIs (área óptica primaria)
st.markdown("# 📊 DSS v1.2 — Soberanía de Datos · DiDi Food")
st.caption(f"N={n_total} jornadas · N válido ROI={n_valido} · Período 2025-12-06 → 2026-01-31")
st.divider()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("ROI Auditado", f"{roi_periodo:.2f}%",
              delta=f"N={n_valido} jornadas válidas",
              delta_color="off")
with col2:
    st.metric("RO Media", f"{ro_media:.3f}x",
              delta=f"Mediana: {ro_mediana:.3f}x",
              delta_color="off")
with col3:
    st.metric("β Modelo", f"${BETA_PEDIDO:,}",
              delta="COP/pedido",
              delta_color="off")
with col4:
    km_fantasma = round(df['km_fantasma'].sum(), 1)
    st.metric("km Fantasma", f"{km_fantasma:,} km",
              delta=f"{round(km_fantasma/df['km_google'].sum()*100,1)}% de divergencia",
              delta_color="off")
with col5:
    prop_bono = round(df['complemento_bono'].sum() / df['garantizado_meta'].sum() * 100, 1)
    st.metric("Ingreso-Arbitraje", f"{prop_bono}%",
              delta="del ingreso bruto",
              delta_color="off")

st.divider()

# ZONA MEDIA: Visualizaciones (centro del patrón Z)
tab1, tab2, tab3, tab4 = st.tabs([
    "📡 Asimetría Algorítmica",
    "📈 HOPs — Regresión Prescriptiva",
    "🎯 Punto de Quiebre RO",
    "📦 Distribución ROI"
])

# ── TAB 1: Asimetría Algorítmica ─────────────────────────────────────────────
with tab1:
    fig1 = go.Figure()
    jornadas = list(range(n_total))
    fig1.add_trace(go.Scatter(
        x=jornadas, y=df['km_google'],
        name='km Reales (Google Maps)', line=dict(color=COLOR_GRIS, width=2),
        fill=None
    ))
    fig1.add_trace(go.Scatter(
        x=jornadas, y=df['km_didi'],
        name=f"km Percibidos (DiDi · RO={ro_media:.3f}x)",
        line=dict(color=COLOR_AZUL, width=2.5),
        fill='tonexty', fillcolor='rgba(52,152,219,0.15)'
    ))
    fig1.update_layout(
        title=dict(
            text=f"La asimetría algorítmica genera {round(df['km_fantasma'].sum()/df['km_google'].sum()*100,1)}% de distancia fantasma",
            font=dict(size=14, color=COLOR_TEXTO)
        ),
        xaxis_title="Jornada Operativa",
        yaxis_title="Kilómetros",
        plot_bgcolor='white', paper_bgcolor='white',
        showlegend=True, legend=dict(x=0.01, y=0.99),
        yaxis=dict(rangemode='tozero'),
        xaxis=dict(showgrid=False),
    )
    fig1.update_xaxes(showgrid=False)
    fig1.update_yaxes(showgrid=False, zeroline=True, zerolinewidth=1)
    # Anotaciones directas Tufte
    fig1.add_annotation(
        x=0.02, y=0.95, xref='paper', yref='paper',
        text=f"km Reales: {round(df['km_google'].sum()):,} km",
        showarrow=False, font=dict(color=COLOR_GRIS, size=11)
    )
    fig1.add_annotation(
        x=0.02, y=0.88, xref='paper', yref='paper',
        text=f"km Percibidos: {round(df['km_didi'].sum()):,} km",
        showarrow=False, font=dict(color=COLOR_AZUL, size=11)
    )
    fig1.add_annotation(
        x=0.02, y=0.81, xref='paper', yref='paper',
        text=f"km Fantasma: {round(df['km_fantasma'].sum()):,} km",
        showarrow=False, font=dict(color=COLOR_ROJO, size=11, weight='bold')
    )
    st.plotly_chart(fig1, use_container_width=True)

# ── TAB 2: HOPs ──────────────────────────────────────────────────────────────
with tab2:
    st.markdown(f"""
    **Hypothetical Outcome Plots (HOPs)** — {n_hops} trayectorias simuladas
    
    Cada línea gris representa una trayectoria plausible del modelo `utilidad_neta ~ β×pedidos + ε`
    con `ε ~ N(0, σ={SIGMA_RESIDUAL:,})`. El punto rojo es tu proyección de hoy.
    El rango sombreado captura el 90% de los resultados posibles.
    """)
    fig2 = go.Figure()
    # Trazar HOPs (líneas grises semitransparentes)
    for i in range(n_hops):
        fig2.add_trace(go.Scatter(
            x=pedidos_range, y=hops_matrix[i],
            mode='lines', line=dict(color='rgba(200,200,200,0.3)', width=1),
            showlegend=False, hoverinfo='skip'
        ))
    # Línea media OLS
    y_media = BETA_PEDIDO * pedidos_range + INTERCEPTO
    fig2.add_trace(go.Scatter(
        x=pedidos_range, y=y_media,
        mode='lines', name=f'y = {BETA_PEDIDO:,}x + ({INTERCEPTO:,})',
        line=dict(color=COLOR_AZUL, width=3)
    ))
    # Banda IC 90%
    y_p5  = np.percentile(hops_matrix, 5, axis=0)
    y_p95 = np.percentile(hops_matrix, 95, axis=0)
    fig2.add_trace(go.Scatter(
        x=np.concatenate([pedidos_range, pedidos_range[::-1]]),
        y=np.concatenate([y_p95, y_p5[::-1]]),
        fill='toself', fillcolor='rgba(52,152,219,0.15)',
        line=dict(color='rgba(0,0,0,0)'),
        name='IC 90% (HOPs)',
        showlegend=True
    ))
    # Puntos del dataset histórico
    fig2.add_trace(go.Scatter(
        x=df['pedidos_fisicos'], y=df['utilidad_neta'],
        mode='markers', name='Jornadas históricas',
        marker=dict(color=COLOR_AZUL, size=8, opacity=0.7,
                    line=dict(color='white', width=1))
    ))
    # Proyección actual (punto rojo)
    fig2.add_trace(go.Scatter(
        x=[pedidos_input], y=[util_ajustada],
        mode='markers+text', name='Proyección hoy',
        marker=dict(color=COLOR_ROJO, size=14, symbol='star',
                    line=dict(color='white', width=2)),
        text=[f'${util_ajustada:,}'], textposition='top center',
        textfont=dict(color=COLOR_ROJO, size=12)
    ))
    fig2.update_layout(
        title=dict(
            text=f"pedidos_fisicos={pedidos_input} → utilidad esperada: ${util_ajustada:,} COP (ajuste eficiencia: {factor_ef})",
            font=dict(size=13)
        ),
        xaxis_title="Pedidos Físicos Completados",
        yaxis_title="Utilidad Neta (COP)",
        plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(rangemode='tozero', tickprefix='$', tickformat=','),
        xaxis=dict(showgrid=False),
    )
    fig2.update_yaxes(showgrid=False)
    fig2.update_xaxes(showgrid=False)
    st.plotly_chart(fig2, use_container_width=True)

# ── TAB 3: Punto de Quiebre RO ───────────────────────────────────────────────
with tab3:
    fig3 = go.Figure()
    # Zona óptima (sombreado verde)
    fig3.add_vrect(
        x0=RO_OPTIMO_MIN, x1=RO_OPTIMO_MAX,
        fillcolor="rgba(46,204,113,0.15)", line_width=0,
        annotation_text="Zona Óptima", annotation_position="top left",
        annotation_font_color=COLOR_VERDE
    )
    # Línea umbral crítico
    fig3.add_vline(x=RO_CRITICO, line_dash='dash', line_color=COLOR_ROJO,
                   annotation_text="Umbral Crítico (RO=2.0)",
                   annotation_font_color=COLOR_ROJO)
    # Scatter por zona
    colores_zona = df['ratio_optimizacion'].apply(
        lambda r: COLOR_VERDE if RO_OPTIMO_MIN <= r <= RO_OPTIMO_MAX
                  else (COLOR_ROJO if r >= RO_CRITICO else COLOR_GRIS)
    )
    fig3.add_trace(go.Scatter(
        x=df['ratio_optimizacion'], y=df['eficiencia_cumplimiento'],
        mode='markers',
        marker=dict(color=colores_zona, size=10, opacity=0.85,
                    line=dict(color='white', width=1)),
        text=[f"RO={r:.2f} · Efic={e:.2%}" for r, e in
              zip(df['ratio_optimizacion'], df['eficiencia_cumplimiento'])],
        hoverinfo='text', showlegend=False
    ))
    # Línea RO input actual
    fig3.add_vline(x=ro_input, line_dash='dot', line_color=COLOR_AZUL,
                   annotation_text=f"RO hoy: {ro_input:.2f}",
                   annotation_font_color=COLOR_AZUL)
    # Anotaciones eficiencia por zona
    ef_opt  = df.loc[(df['ratio_optimizacion']>=RO_OPTIMO_MIN) & (df['ratio_optimizacion']<=RO_OPTIMO_MAX), 'eficiencia_cumplimiento'].mean()
    ef_crit = df.loc[df['ratio_optimizacion']>=RO_CRITICO, 'eficiencia_cumplimiento'].mean()
    if not np.isnan(ef_opt):
        fig3.add_annotation(x=1.785, y=1.05, text=f"Efic. Óptima: {ef_opt:.1%}",
                            showarrow=False, font=dict(color=COLOR_VERDE, size=11))
    if not np.isnan(ef_crit):
        fig3.add_annotation(x=2.15, y=1.05, text=f"Efic. Crítica: {ef_crit:.1%}",
                            showarrow=False, font=dict(color=COLOR_ROJO, size=11))
    fig3.update_layout(
        title="Punto de Quiebre: La eficiencia colapsa cuando el RO supera 2.0",
        xaxis_title="Ratio de Optimización (RO = km_didi / km_google)",
        yaxis_title="Eficiencia de Cumplimiento",
        plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(tickformat='.0%', rangemode='tozero'),
        xaxis=dict(showgrid=False),
    )
    fig3.update_yaxes(showgrid=False)
    st.plotly_chart(fig3, use_container_width=True)

# ── TAB 4: Raincloud ROI ─────────────────────────────────────────────────────
with tab4:
    roi_vals  = df['roi_diario'].dropna()
    n_nan     = df['roi_diario'].isna().sum()
    roi_medio = round(roi_vals.mean(), 2)
    roi_med   = round(roi_vals.median(), 2)
    fig4 = go.Figure()
    # Strip plot (puntos individuales)
    jitter = np.random.uniform(-0.05, 0.05, len(roi_vals))
    fig4.add_trace(go.Scatter(
        x=roi_vals, y=jitter - 0.3,
        mode='markers', name='Jornadas individuales',
        marker=dict(color=COLOR_AZUL, size=8, opacity=0.6,
                    line=dict(color='white', width=1))
    ))
    # Boxplot
    fig4.add_trace(go.Box(
        x=roi_vals, y0=0, name='Distribución ROI',
        boxpoints=False, line=dict(color=COLOR_GRIS, width=1.5),
        fillcolor='rgba(200,200,200,0.3)',
        median=dict(color=COLOR_ROJO, width=2)
    ))
    # Línea mediana
    fig4.add_vline(x=roi_med, line_dash='dash', line_color=COLOR_ROJO,
                   annotation_text=f"Mediana: {roi_med:.1f}%",
                   annotation_font_color=COLOR_ROJO)
    # Anotación Brecha de Integridad
    fig4.add_annotation(
        x=roi_vals.max() * 0.75, y=0.35,
        text=f"⚠ Brecha de Integridad: {n_nan} jornadas<br>(Gasto $0 → ROI = NaN)",
        showarrow=False,
        bgcolor='rgba(231,76,60,0.15)', bordercolor=COLOR_ROJO,
        font=dict(color=COLOR_ROJO, size=11)
    )
    fig4.update_layout(
        title=f"ROI auditado: {roi_medio:.2f}% (media) · {roi_med:.2f}% (mediana) · N válido={len(roi_vals)}",
        xaxis_title="ROI Diario (%)",
        yaxis=dict(visible=False, range=[-0.6, 0.6]),
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(rangemode='tozero', showgrid=False),
        showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# ZONA INFERIOR — PANEL DE DECISIÓN BINARIZADA (área terminal del patrón Z)
# ─────────────────────────────────────────────────────────────────────────────

st.divider()
st.markdown("## 🎯 Panel de Decisión Binarizada — Capa 4 DSS")

col_decision, col_detalle, col_contexto = st.columns([1.2, 1.5, 1.3])

with col_decision:
    st.markdown(f"""
    <div class="{decision_class}">
        <h1 style="font-size:2rem; margin:0">{decision}</h1>
        <p style="color:#BDC3C7; margin-top:8px; font-size:0.9rem">{razon}</p>
    </div>
    """, unsafe_allow_html=True)

with col_detalle:
    st.markdown("**Variables de entrada procesadas:**")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Pedidos proyectados", pedidos_input)
        st.metric("Utilidad esperada", f"${util_ajustada:,}",
                  delta=f"Factor efic.: {factor_ef}" if factor_ef < 1.0 else None,
                  delta_color="inverse" if factor_ef < 1.0 else "off")
        st.metric("Franja horaria",
                  "🔥 PICO" if es_pico else "🌙 VALLE",
                  delta="Hora óptima" if es_pico else "Hora sub-óptima",
                  delta_color="normal" if es_pico else "inverse")
    with col_b:
        st.metric("RO ingresado", f"{ro_input:.2f}x")
        st.metric("Zona RO",
                  "✅ Óptima" if zona_opt else ("🔴 Crítica" if alerta else "🟡 Neutral"),
                  delta=f"[{RO_OPTIMO_MIN}–{RO_OPTIMO_MAX}]" if zona_opt else
                        (f"≥{RO_CRITICO}" if alerta else "Monitorear"))
        st.metric("σ residual", f"${SIGMA_RESIDUAL:,}",
                  delta="Error estándar modelo", delta_color="off")

with col_contexto:
    st.markdown("**Contexto histórico del período:**")
    jornadas_optimas = int(df['zona_arbitraje_optima'].sum())
    jornadas_criticas = int(df['alerta_critica'].sum())
    jornadas_pico = int(df['franja_pico'].sum())
    st.metric("Jornadas en zona óptima", f"{jornadas_optimas}/{n_total}",
              delta=f"{round(jornadas_optimas/n_total*100,1)}% del período",
              delta_color="normal")
    st.metric("Jornadas en zona crítica", f"{jornadas_criticas}/{n_total}",
              delta=f"{round(jornadas_criticas/n_total*100,1)}% del período",
              delta_color="inverse")
    st.metric("Jornadas en franja PICO", f"{jornadas_pico}/{n_total}",
              delta=f"{round(jornadas_pico/n_total*100,1)}% del período",
              delta_color="normal")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.divider()
st.caption(
    "DSS v1.2 · Infraestructura Operativa de Datos · DiDi Food · San Cristóbal Sur, Bogotá D.C. · "
    "β=$14,940 COP/pedido · σ=$51,320 COP · ROI Auditado · Principio: Transparencia Radical"
)
