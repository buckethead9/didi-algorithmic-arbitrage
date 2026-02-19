# QUICKSTART — DSS v1.2
## Instalación y operación en 10 minutos

**Sistema:** DiDi Food · Soberanía de Datos · Bogotá D.C.

---

## REQUISITOS

```
Python 3.8+     →  python --version
pip             →  pip --version
~50 MB disco    →  dependencias + dataset
Navegador web   →  para la interfaz Streamlit
```

---

## INSTALACIÓN (3 pasos)

```bash
# 1. Clonar el repositorio
git clone https://github.com/buckethead9/didi-algorithmic-arbitrage.git
cd didi-algorithmic-arbitrage

# 2. Instalar dependencias
pip install pandas numpy scipy streamlit plotly --break-system-packages

# 3. Verificar instalación
python -c "import pandas, numpy, scipy, streamlit, plotly; print('✅ Todo instalado')"
```

---

## USO BÁSICO

```bash
# Generar dataset procesado (28 variables · recalibra invariantes)
python src/main.py

# Lanzar DSS v1.2 (interfaz de decisión)
streamlit run src/app_copiloto.py
# → Abre http://localhost:8501 en el navegador

# Cargar a MySQL (opcional)
mysql -u root -p nombre_base < sql/queries_auditoria.sql
```

---

## AGREGAR NUEVA JORNADA (N+1)

```bash
# 1. Edita el CSV crudo
echo "2026-02-18,17:01,23:45,63.08,107.40,143000,10,1,18000" >> data/raw/didi_analisis_12_01.csv

# 2. Recalibra el modelo
python src/main.py

# 3. El DSS usa los invariantes actualizados automáticamente
```

---

## ÁRBOL DE ARCHIVOS

```
didi-algorithmic-arbitrage/
├── README.md                           ← Punto de entrada · Fe de Erratas
├── src/
│   ├── main.py                         ← ETL + Feature Engineering (28 vars)
│   └── app_copiloto.py                 ← DSS v1.2 (Streamlit + Plotly + HOPs)
├── data/
│   ├── raw/didi_analisis_12_01.csv     ← Dataset crudo (9 columnas)
│   └── processed/didi_procesado_v1.1.csv ← Dataset MECE (28 columnas)
├── docs/
│   ├── auditoria_integridad_v1.2.md    ← Núcleo forense
│   ├── RESUMEN_TECNICO_v1.2.md         ← Executive Brief (7S McKinsey)
│   ├── diccionario_variables_MECE.md   ← Taxonomía 28 variables
│   ├── visualizaciones_tufte.md        ← Defensa visual (Tufte + HOPs)
│   ├── protocolo_accion_usuario.md     ← Ingesta Capa 4 DSS
│   └── QUICKSTART.md                   ← Este archivo
└── sql/
    └── queries_auditoria.sql           ← MySQL 8.0+ · CASE sincronizados
```

---

**Soporte:** Revisa `docs/protocolo_accion_usuario.md` para el protocolo completo de captura.  
**Errores:** Los errores del pipeline se imprimen al stdout con prefijo `[ETL ERROR]`.
