# streamlit_water_quality_app.py
# Streamlit app para evaluar calidad de agua

import streamlit as st
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Comprobador de calidad de agua", layout="centered")

st.title("Comprobador de calidad de agua")
st.markdown(
    "Ingresa los valores medidos de pH, turbidez (NTU) y arsénico (µg/L). "
    "La app calcula un índice sencillo de calidad y muestra anuncios y recomendaciones."
)

REFERENCE = {
    'pH': {'min': 6.5, 'max': 8.5},
    'turbidity': {'good': 1.0, 'acceptable': 5.0},
    'arsenic': {'guideline': 10.0}
}

col1, col2, col3 = st.columns(3)
with col1:
    ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1, format="%.2f")
with col2:
    turbidity = st.number_input("Turbidez (NTU)", min_value=0.0, value=0.5, step=0.1, format="%.2f")
with col3:
    arsenic = st.number_input("Arsénico (µg/L)", min_value=0.0, value=5.0, step=0.1, format="%.2f")

st.markdown("---")

def assess_ph(value):
    if REFERENCE['pH']['min'] <= value <= REFERENCE['pH']['max']:
        return ('OK', 100, 'pH dentro del rango recomendado.')
    return ('FUERA', 50, f'pH fuera de rango ({value}).')

def assess_turbidity(value):
    if value <= REFERENCE['turbidity']['good']:
        return ('OK', 100, 'Turbidez ideal < 1 NTU.')
    elif value <= REFERENCE['turbidity']['acceptable']:
        return ('PRECAUCIÓN', 70, f'Turbidez moderada ({value} NTU).')
    return ('FUERA', 30, f'Turbidez elevada ({value} NTU).')

def assess_arsenic(value):
    if value <= REFERENCE['arsenic']['guideline']:
        return ('OK', 100, 'Arsénico por debajo del límite guía.')
    return ('FUERA', 0, f'Arsénico alto: {value} µg/L.')

def compute_wqi(scores, weights=None):
    if weights is None:
        weights = {'pH': 0.25, 'turbidity': 0.25, 'arsenic': 0.5}
    return sum(scores[k] * weights[k] for k in scores)

assessments = {
    'pH': assess_ph(ph),
    'turbidity': assess_turbidity(turbidity),
    'arsenic': assess_arsenic(arsenic)
}

scores = {k: v[1] for k,v in assessments.items()}
wqi = compute_wqi(scores)

if assessments['arsenic'][0] == 'FUERA':
    decision = 'NO APTA'
    decision_text = 'El agua NO es apta para consumo humano por arsénico elevado.'
elif wqi >= 85 and all(a[0]=='OK' for a in assessments.values()):
    decision = 'APTA'
    decision_text = 'El agua es apta para consumo humano.'
elif wqi >= 60:
    decision = 'APTA CON PRECAUCIÓN'
    decision_text = 'El agua puede consumirse con tratamiento adicional.'
else:
    decision = 'NO APTA'
    decision_text = 'El agua NO es apta sin tratamiento adicional.'

st.markdown("### Resultado")
if decision == 'APTA':
    st.success(f"{decision} — {decision_text}")
elif decision == 'APTA CON PRECAUCIÓN':
    st.warning(f"{decision} — {decision_text}")
else:
    st.error(f"{decision} — {decision_text}")

st.markdown("---")
st.subheader("Detalles por parámetro")
for k,v in assessments.items():
    st.write(f"**{k}**: {v[0]} — {v[2]} (puntaje {v[1]})")

st.markdown("---")
st.write(f"Índice simple de calidad (0-100): **{wqi:.1f}**")

report = f"""Informe de calidad de agua
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Lecturas:
 - pH: {ph}
 - Turbidez: {turbidity} NTU
 - Arsénico: {arsenic} µg/L

Resultado final: {decision}
{decision_text}
"""

st.download_button("Descargar informe (TXT)", data=report, file_name="informe_calidad_agua.txt", mime="text/plain")
