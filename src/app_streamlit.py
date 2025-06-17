import streamlit as st
import requests

# Título principal de la aplicación
st.title("Pregúntale a tu LLM con imagen (Ollama + FastAPI)")

# Campo de texto para que el usuario escriba su pregunta
question = st.text_input("Pregunta:")
# Campo para subir una imagen opcional (jpg, jpeg, png)
uploaded_file = st.file_uploader(
  "Sube una imagen (opcional)", type=["jpg", "jpeg", "png"]
)

# Si el usuario sube una imagen, se muestra en la interfaz
if uploaded_file:
  st.image(uploaded_file, caption="Imagen subida", use_container_width=True)

# Botón para enviar la pregunta (y la imagen, si existe) a la API
if st.button("Enviar"):
  if not question:
    # Advertencia si el campo de pregunta está vacío
    st.warning("Por favor, escribe una pregunta.")
  else:
    files = None
    # Si hay imagen, se prepara el archivo para enviarlo en la petición
    if uploaded_file:
      files = {
        "file": (
          uploaded_file.name,
          uploaded_file.getvalue(),
          uploaded_file.type,
        )
      }
    data = {"question": question}
    try:
      # Se realiza la petición POST a la API FastAPI
      response = requests.post(
        "http://localhost:8000/api/question", data=data, files=files
      )
      if response.ok:
        # Si la respuesta es exitosa, se muestran los resultados
        result = response.json()
        st.success(f"Respuesta: {result['answer']}")
        st.info(f"Razonamiento: {result['thoughts']}")
        st.write(f"Tema: {result['topic']}")
      else:
        # Si la API responde con error, se muestra el mensaje
        st.error(f"Error: {response.text}")
    except Exception as e:
      # Si no se puede conectar con la API, se muestra un error
      st.error(f"No se pudo conectar con la API: {e}")
