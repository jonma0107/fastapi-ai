# API IA - FastAPI + Ollama

## 🚀 Inicio rápido con Docker

Este proyecto utiliza **Docker** para facilitar la ejecución y despliegue de una API basada en FastAPI que interactúa con modelos LLM de **Ollama**.

- El archivo `Dockerfile` define el entorno Python, instala dependencias con Poetry y expone el puerto 8000 para la API.
- El archivo `docker-compose.yml` permite levantar el servicio fácilmente, usando el modo de red `host` para que el contenedor pueda comunicarse con Ollama corriendo en tu máquina.

### Pasos para levantar la API

1. **Asegúrate de tener Docker y Docker Compose instalados.**
2. **Asegúrate de que Ollama esté corriendo en tu host** (por ejemplo, con `ollama serve`).
3. **Levanta la API:**
   ```bash
   docker compose up --build
   ```
4. Accede a la documentación interactiva en: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 ¿Qué hace la API? (`src/ollama_app.py`)

Esta API expone un endpoint inteligente que permite enviar una **pregunta** junto con una **imagen**. El backend procesa la imagen, consulta un modelo LLM de Ollama y devuelve una respuesta enriquecida y estructurada.

### **Lógica principal:**

- **Modelos de datos:**  
  Se definen modelos Pydantic para estructurar tanto la pregunta como la respuesta. La respuesta incluye:
  - La respuesta directa (`answer`)
  - El razonamiento del modelo (`thoughts`)
  - El tema identificado (`topic`)

- **Procesamiento de la imagen:**  
  La imagen enviada se convierte automáticamente a base64 para ser entendida por el modelo LLM.

- **Interacción con Ollama:**  
  Se consulta un modelo LLM de Ollama (por defecto, `gemma3:latest`), pidiéndole que responda **siempre en formato JSON** con los campos esperados.

- **Validación y logging:**  
  La respuesta del modelo se valida y estructura antes de devolverse al usuario. Además, cada interacción se registra en un archivo de log para auditoría y análisis.

- **Endpoint principal:**  
  - **POST `/api/question`**  
    Recibe:
    - `question`: Texto de la pregunta (campo de formulario)
    - `file`: Imagen a analizar (archivo)
    Devuelve:
    - Respuesta estructurada con la respuesta, razonamiento y tema.

---

## 📄 Ejemplo de uso en Swagger

1. Ve a [http://localhost:8000/docs](http://localhost:8000/docs)
2. Usa el endpoint `/api/question`
3. Escribe tu pregunta y sube una imagen.
4. Obtendrás una respuesta enriquecida y explicada por el modelo.

---

## 📝 Notas

- Es necesario que el servidor Ollama esté corriendo y accesible desde el contenedor Docker.
- El endpoint espera siempre una imagen y una pregunta; ambos son obligatorios. 