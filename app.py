import google.generativeai as genai
import PIL.Image
import streamlit as st

st.set_page_config(
    page_title="Lector Automático de Planillas - Colectivos", page_icon="🚌"
)

st.title("🚌 Lector Automático de Planillas con IA")
st.write(
    "Subí la foto de la planilla del chofer. La inteligencia artificial"
    " detectará automáticamente la línea, el ramal (Línea 20: 1, A, B; Línea"
    " 188: A, B, E, C, G), los tachones y calculará los kilómetros."
)

# 1. Casillero para la clave de API gratuita de Google AI Studio
api_key = st.text_input(
    "Ingresá tu clave de API de Google AI Studio (Gratis):",
    type="password",
    help="Obtenela gratis en aistudio.google.com",
)

# 2. Subir la foto primero
archivo_foto = st.file_uploader(
    "Subir foto de la planilla del chofer", type=["jpg", "jpeg", "png"]
)

if archivo_foto is not None:
  # Mostrar la imagen cargada en pantalla
  imagen = PIL.Image.open(archivo_foto)
  st.image(
      imagen,
      caption="Planilla del chofer cargada para análisis",
      use_column_width=True,
  )

  if not api_key:
    st.warning(
        "⚠️ Por favor, ingresá tu clave de API arriba para que la IA pueda"
        " leer la foto."
    )
  else:
    if st.button("🔍 Analizar planilla automáticamente"):
      with st.spinner(
          "Leyendo tramos, tachones, detectando línea y ramales con IA..."
      ):
        try:
          # Configurar la API de Google con la clave ingresada
          genai.configure(api_key=api_key)
          # Utilizar el modelo de visión gratuito y rápido
          model = genai.GenerativeModel("gemini-1.5-flash")

          # Instrucción experta para que la IA entienda las líneas, ramales y tachones
          prompt = (
              "Analiza esta planilla de colectivos de Buenos Aires. "
              "Detecta automáticamente si pertenece a la Línea 20 (Ramales: 1, A,"
              " B) o a la Línea 188 (Ramales: A, B, E, C, G). "
              "Interpreta los tramos, fragmentos y tachones escritos a mano en"
              " el papel. "
              "Calcula los kilómetros totales, los kilómetros muertos y los"
              " kilómetros netos basados en las distancias oficiales de ese"
              " ramal. "
              "Devuelve la respuesta estructurada de forma clara indicando:"
              " Línea detectada, Ramal detectado, Kilómetros Totales,"
              " Kilómetros Muertos y Kilómetros Netos."
          )

          response = model.generate_content([prompt, imagen])

          st.success("¡Análisis completado con éxito!")
          st.markdown("### 📊 Resultado del Análisis:")
          st.write(response.text)

        except Exception as e:
          st.error(
              f"Ocurrió un error al procesar la imagen con la API: {e}"
          )

