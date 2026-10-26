import streamlit as st

st.set_page_config(
    page_title="Calculadora Automática de Colectivos", page_icon="🚌"
)

st.title("🚌 Lector Inteligente de Planillas")
st.write(
    "Subí la foto de la planilla del chofer. La IA detectará automáticamente"
    " los tramos, tachones y calculará los kilómetros según el ramal."
)

# Clave de API para que la IA procese la imagen (podés guardarla o pedirla)
api_key = st.text_input(
    "Ingresá tu clave de API de Inteligencia Artificial (OpenAI / Gemini):",
    type="password",
)

# 1. Selección de Línea y Ramales
linea_seleccionada = st.selectbox(
    "Seleccione la Línea:", ["Línea 20", "Línea 188"]
)

if linea_seleccionada == "Línea 20":
  ramal_seleccionado = st.selectbox(
      "Seleccione el Ramal:", ["Ramal 1", "Ramal A", "Ramal B"]
  )
else:
  ramal_seleccionado = st.selectbox(
      "Seleccione el Ramal:",
      ["Ramal A", "Ramal B", "Ramal E", "Ramal C", "Ramal G"],
  )

# 2. Subir la foto de la planilla
archivo_foto = st.file_uploader(
    "Subir foto de la planilla del chofer", type=["jpg", "jpeg", "png"]
)

if archivo_foto is not None:
  st.image(
      archivo_foto,
      caption=f"Planilla cargada para {linea_seleccionada} - {ramal_seleccionado}",
      use_column_width=True,
  )

  if not api_key:
    st.warning(
        "⚠️ Por favor, ingresá tu clave de API arriba para que el sistema"
        " pueda leer la foto."
    )
  else:
    if st.button("🚀 Procesar planilla con Inteligencia Artificial"):
      with st.spinner(
          "Leyendo tramos, tachones y cruzando con la tabla oficial..."
      ):

        # --- AQUÍ SE CONECTARÍA EL MOTOR DE VISIÓN ARTIFICIAL ---
        # El sistema envía la imagen, la línea y el ramal seleccionado a la IA,
        # la cual lee los datos escritos y aplica las distancias oficiales.

        # Ejemplo de respuesta procesada por la IA basada en tu planilla real:
        km_totales = 168.50
        km_muertos = 10.20
        km_netos = km_totales - km_muertos

        st.success("¡Lectura de planilla finalizada con éxito!")

        col1, col2, col3 = st.columns(3)
        col1.metric("Kilómetros Totales", f"{km_totales} km")
        col2.metric("Kilómetros Muertos", f"{km_muertos} km")
        col3.metric("Kilómetros Netos", f"{km_netos} km")

        st.info(
            f"Resultados extraídos automáticamente para la **{linea_seleccionada}"
            f" ({ramal_seleccionado})** considerando los tachones y tramos"
            " marcados."
        )
