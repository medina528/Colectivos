import streamlit as st

st.title("Calculadora de Kilómetros - Colectivos")

linea = st.selectbox("Seleccione la Línea:", ["Línea 188", "Línea 20"])

st.write(f"Calculadora activa para la **{linea}**")

km_inicio = st.number_input("Kilómetros al iniciar la jornada:", min_value=0.0, step=0.5)
km_fin = st.number_input("Kilómetros al finalizar la jornada:", min_value=0.0, step=0.5)
km_muertos = st.number_input("Kilómetros muertos o de enlace:", min_value=0.0, step=0.5)

if st.button("Calcular Kilómetros Netos"):
    km_brutos = km_fin - km_inicio
    km_netos = km_brutos - km_muertos
    if km_netos < 0:
        st.error("Error: Los kilómetros netos no pueden dar negativos. Verifique los números.")
    else:
        st.success(f"¡Cálculo realizado para la {linea}!")
        st.write(f"- Kilómetros totales (brutos): {km_brutos} km")
        st.write(f"- Descuento por kilómetros muertos: {km_muertos} km")
        st.markdown(f"### Kilómetros Netos Trabajados: **{km_netos} km**")
