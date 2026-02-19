# PROTOCOLO DE ACCIÓN DEL USUARIO — DSS v1.2
## Ingesta en Capa 4 · Decisiones en Tiempo Real

**Sistema:** DiDi Food · San Cristóbal Sur · Bogotá D.C.  
**Versión:** 1.2 · **Publicado:** 2026-02-18  
**Tiempo de ingesta:** ~5 minutos por jornada

---

## PASO 1: CAPTURA DE DATOS EN CAMPO (Durante la jornada)

Registra estas 9 variables en una nota de celular o libreta durante la jornada:

```
┌─────────────────────────────────────────────────────┐
│  VARIABLES A CAPTURAR (9 campos)                    │
├─────────────────────────────────────────────────────┤
│  fecha         →  YYYY-MM-DD     Ej: 2026-02-18     │
│  h_inicio      →  HH:MM          Ej: 17:01          │
│  h_fin         →  HH:MM          Ej: 23:45          │
│  km_google     →  Google Maps    Ej: 63.08          │
│  km_didi       →  App DiDi       Ej: 107.4          │
│  ingreso_bruto →  App DiDi       Ej: 143000         │
│  pedidos_cohete→  Conteo manual  Ej: 10             │
│  pedidos_norm. →  Conteo manual  Ej: 1              │
│  gasto_extra   →  Recibo físico  Ej: 18000          │
└─────────────────────────────────────────────────────┘
```

### Cómo obtener km_google

1. Abre Google Maps en tu celular
2. Al finalizar la jornada, ve a Configuración → Tu perfil → Línea de tiempo
3. Selecciona el día → verás los km recorridos
4. Regístralos con 2 decimales (Ej: 63.08)

### Cómo obtener km_didi

1. En la app DiDi, ve al Resumen del día (o historial de jornada)
2. Captura el valor de kilómetros que muestra la app
3. Este valor puede diferir significativamente de km_google — eso es normal y esperado

---

## PASO 2: INGRESO AL CSV (Post-jornada · ~2 minutos)

Abre `data/raw/didi_analisis_12_01.csv` y agrega una fila al final:

```csv
2026-02-18,17:01,23:45,63.08,107.40,143000,10,1,18000
```

**Reglas críticas:**
- `h_inicio` y `h_fin`: formato `HH:MM` (24 horas) — NO decimales (8.52 es incorrecto; correcto: 08:31)
- Si terminas después de medianoche: `h_fin` puede ser `00:12`, `01:30`, etc. — el pipeline lo detecta automáticamente
- `gasto_extra = 0` si no tuviste gastos ese día — NO dejes la celda vacía

---

## PASO 3: EJECUTAR PIPELINE ETL (Recalibración N+1)

```bash
cd didi-algorithmic-arbitrage
python src/main.py
```

**Salida esperada:**
```
✅ Dataset cargado: N+1 observaciones
✅ Dataset procesado exportado: data/processed/didi_procesado_v1.1.csv
ROI del Período: XXX.XX%  [AUDITADO · N_válido=XX]
RO Media:        X.XXXx
β (recalibrado): $XX,XXX COP/pedido
✅ PIPELINE v1.2 COMPLETADO — 28 columnas exportadas
```

---

## PASO 4: INGESTA EN EL DSS (Decisión Binarizada)

```bash
streamlit run src/app_copiloto.py
```

Abre el navegador en `http://localhost:8501` y completa el panel lateral:

```
┌─────────────────────────────────────────────────────┐
│  PANEL LATERAL DSS — CAPA 4                         │
├─────────────────────────────────────────────────────┤
│  Pedidos físicos proyectados    [slider: 1–25]      │
│  RO observado en tu zona        [número: 0.50–3.50] │
│  Hora de inicio proyectada      [selector HH:00]    │
│  Trayectorias HOPs a simular    [slider: 20–100]    │
└─────────────────────────────────────────────────────┘
```

**El DSS entregará inmediatamente una de las cuatro decisiones:**

| Decisión | Condición | Acción |
|---|---|---|
| ✅ **SÍ OPERAR** | 1.73 ≤ RO ≤ 1.84 | Continuar · Mantener posición en zona actual |
| 🔴 **NO OPERAR** | RO ≥ 2.0 | Cambiar de zona inmediatamente |
| ⚠️ **EVALUAR VIABILIDAD** | RO < 1.30 | Verificar activación del bono antes de continuar |
| 🟡 **MONITOREAR** | Otros rangos | Continuar con vigilancia de RO |

---

## PASO 5: LECTURA DE LOS HOPs (Interpretación de Incertidumbre)

El gráfico de HOPs muestra **50 trayectorias posibles** de tu utilidad según los pedidos que proyectas completar.

**Lectura correcta:**
```
"Si proyecto 13 pedidos, mi utilidad está en el rango sombreado con
 90% de probabilidad. La línea azul es el centro del rango, no una garantía."
```

**Por qué NO leer los HOPs como una cifra exacta:**
- El modelo tiene un error estándar de ~$27,707 COP por jornada
- Cada jornada tiene variaciones de tráfico, clima, demanda, etc.
- El rango sombreado captura el 90% de los resultados históricos observados

---

## REFERENCIA RÁPIDA — UMBRALES OPERATIVOS

```
┌────────────────────────────────────────────────────────────┐
│  UMBRALES DSS v1.2 (Invariantes — No modificar)            │
├────────────────────────────────────────────────────────────┤
│  Zona Óptima:    1.73 ≤ RO ≤ 1.84   → ✅ SÍ OPERAR        │
│  Zona Crítica:   RO ≥ 2.0           → 🔴 NO OPERAR        │
│  Franja PICO:    17:00 – 20:59      → Alta densidad        │
│  β modelo:       $14,940 COP/pedido → Ingreso marginal      │
│  σ residual:     $51,320 COP        → Varianza esperada     │
│  Factor efic.:   0.973              → Ajuste RO ≥ 2.0      │
└────────────────────────────────────────────────────────────┘
```

---

## PREGUNTAS FRECUENTES

**¿Por qué mi km_didi siempre es mayor que km_google?**  
El algoritmo de DiDi calcula distancias con una metodología diferente a Google Maps, incluyendo kilómetros de posicionamiento y ruta algorítmica. Esta diferencia es el substrato del `complemento_bono`. Es sistemática, no un error.

**¿Qué hago si olvidé registrar los gastos de un día?**  
Ingresa `0` en `gasto_extra`. El pipeline marcará esa jornada con `flag_gasto_cero=1` y excluirá el ROI de esa jornada del cálculo del período. **No inventes el valor.**

**¿Con qué frecuencia debo recalibrar el modelo?**  
Cada vez que agregues una nueva jornada. El pipeline recalibra todos los invariantes automáticamente. Para cambios estructurales del mercado (ej: cambio de política de bonos de DiDi), considera reiniciar el dataset.

**¿El DSS garantiza las utilidades proyectadas?**  
No. El DSS entrega probabilidades, no garantías. Los HOPs muestran el rango de resultados plausibles. La decisión binarizada [SÍ/NO OPERAR] reduce el riesgo de operar en zonas sub-óptimas, pero no elimina la incertidumbre de la jornada.

---

**Firmado:**  
*Protocolo de Acción del Usuario v1.2*  
*DSS · DiDi Food · Bogotá D.C. · 2026-02-18*
