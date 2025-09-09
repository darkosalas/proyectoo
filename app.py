
import streamlit as st

# Función para evaluar la calidad del agua
def evaluar_calidad(pH, turbidez, arsenico):
    if arsenico >= 10:
        return "⚠️ Agua NO segura: Arsénico sobre el límite (>=10 µg/L)"
    elif turbidez >= 5:
        return "⚠️ Agua NO segura: Turbidez muy alta (>=5 NTU)"
    elif pH < 6.5 or pH > 8.5:
        return "⚠️ Agua NO segura: pH fuera del rango (6.5 - 8.5)"
    else:
        return "✅ Agua segura para consumo según OMS"

# Interfaz de la app
st.title("💧 Evaluador de Calidad de Agua (OMS)")
st.write("Ingrese los valores de su muestra de agua para evaluar si es segura.")

# Entradas de usuario
pH = st.number_input("pH del agua", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
turbidez = st.number_input("Turbidez (NTU)", min_value=0.0, value=1.0, step=0.1)
arsenico = st.number_input("Arsénico (µg/L)", min_value=0.0, value=5.0, step=0.1)

# Botón de evaluación
if st.button("Evaluar calidad"):
    resultado = evaluar_calidad(pH, turbidez, arsenico)
    st.subheader("Resultado:")
    st.success(resultado) if "✅" in resultado else st.error(resultado)
