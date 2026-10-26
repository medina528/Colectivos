import google.generativeai as genai
import PIL.Image
import streamlit as st

st.set_page_config(
    page_title="Lector Automático de Planillas - Colectivos", page_icon="🚌"
)

st.title("🚌 Lector Automático de Planillas con IA")
st.write(
    "Sacá una foto o subí la planilla del chofer. La inteligencia artificial"
    " detectará automáticamente la línea (20 o 188), los ramales, tachones y"
    " calculará los kilómetros."
)

# 1. Casillero para la clave de API gratuita de Google AI Studio
api_key = st.text_input(
    "Ingresá tu clave de API de Google AI Studio (Gratis):",
    type="password",
    help="Obtenela gratis en aistudio.google.com",
)

# 2. Selector para elegir si usa la cámara nativa o sube archivo
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

if archivo_foto is not None:
  # Mostrar la imagen cargada de forma segura
  imagen = PIL.Image.open(archivo_foto)
  st.image(
      imagen, caption="Planilla lista para procesar", use_container_width=True
  )

  if not api_key:
    st.warning(
        "⚠️ Por favor, ingresá tu clave de API arriba para que la IA pueda"
        " leer la foto."
    )
  else:
    if st.button("🔍 Procesar planilla y calcular"):
      with st.spinner(
          "Analizando ramales, tramos y tachones con inteligencia"
          " artificial..."
      ):
        try:
          genai.configure(api_key=api_key)
          model = genai.GenerativeModel("gemini-1.5-flash")

          prompt = (
              "Analiza esta planilla de colectivos de Buenos Aires. "
              "Detecta automáticamente si pertenece a la Línea 20 (Ramales: 1,"
              " A, B) o a la Línea 188 (Ramales: A, B, E, C, G). "
              "Interpreta los tramos, fragmentos y tachones escritos a"
              " mano. "
              "Calcula los kilómetros totales, kilómetros muertos y"
              " kilómetros netos basados en las distancias oficiales. "
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


