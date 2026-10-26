import google.generativeai as genai
import PIL.Image
import streamlit as st

st.set_page_config(
    page_title="Lector Automático de Planillas - Colectivos", page_icon="🚌"
)

st.title("🚌 Lector Automático de Planillas con IA")
st.write(
    "Sacá una foto o subí la planilla. La inteligencia artificial detectará"
    " automáticamente la línea (20 o 188), los ramales, tachones y calculará"
    " los kilómetros al instante."
)

# Configurar la API de forma automática de fondo (sin que te pida códigos en el celu)
try:
  if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    api_configurada = True
  else:
    api_configurada = False
except Exception:
  api_configurada = False

# Selector para elegir si usa la cámara nativa o sube archivo
metodo = st.radio(
    "¿Cómo querés ingresar la planilla?",
    ["📸 Sacar foto con la cámara", "📁 Seleccionar archivo existente"],
)

archivo_foto = None

if "Cámara" in metodo:
  archivo_foto = st.camera_input("Tomá la foto de la planilla")
else:
  archivo_foto = st.file_uploader(
      "Subir imagen de la planilla", type=["jpg", "jpeg", "png"]
  )

# Procesamiento automático ni bien se carga la foto
if archivo_foto is not None:
  imagen = PIL.Image.open(archivo_foto)
  st.image(
      imagen, caption="Planilla cargada para análisis", use_container_width=True
  )

  if not api_configurada:
    st.error(
        "⚠️ Falta configurar la clave interna en Streamlit Cloud (Secrets)."
    )
  else:
    with st.spinner(
        "Leyendo ramales, tramos y tachones con inteligencia artificial..."
    ):
      try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = (
            "Analiza esta planilla de colectivos de Buenos Aires. "
            "Detecta automáticamente si pertenece a la Línea 20 (Ramales: 1, A,"
            " B) o a la Línea 188 (Ramales: A, B, E, C, G). "
            "Interpreta los tramos, fragmentos y tachones escritos a mano. "
            "Calcula los kilómetros totales, kilómetros muertos y kilómetros"
            " netos basados en las distancias oficiales. "
            "Devuelve la respuesta estructurada indicando claramente: Línea"
            " detectada, Ramal detectado, Kilómetros Totales, Kilómetros"
            " Muertos y Kilómetros Netos."
        )

        response = model.generate_content([prompt, imagen])

        st.success("¡Análisis completado con éxito!")
        st.markdown("### 📊 Resultado del Cálculo:")
        st.write(response.text)

      except Exception as e:
        st.error(
            f"Ocurrió un error al procesar con la API. Detalle técnico: {e}"
        )


