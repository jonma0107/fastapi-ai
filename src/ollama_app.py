from pydantic import BaseModel, Field
import base64
from ollama import chat
import logging
from fastapi import FastAPI, UploadFile, File, Form
import json
# import uvicorn


# Modelos de datos para estructurar la pregunta y la respuesta básica
class QABase(BaseModel):
  question: str = Field(..., description="The question to ask the model")
  answer: str = Field(..., description="The answer provided by the model")


# Modelo extendido que incluye razonamiento y tema de la respuesta
class QAAnalytics(QABase):
  thoughts: str = Field(
    ..., description="The reasoning or thought process behind the answer"
  )
  topic: str = Field(..., description="The topic of the question")


# Utilidad para codificar una imagen a base64 desde un path
def encode_image_to_base64(image_path: str) -> str:
  """Encodes an image file to a base64 string."""
  with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
  return encoded_string


# Función para interactuar con el modelo LLM de Ollama, solicitando respuesta en JSON estructurado
def ollama_llm_response(question: str, encode_image: str) -> str:
  """Generates a response from the Ollama LLM."""
  return chat(
    model="gemma3:latest",
    format=QAAnalytics.model_json_schema(),
    messages=[
      {
        "role": "system",
        "content": "Eres un asistente útil. Responde SIEMPRE en formato JSON con los campos: question, answer, thoughts, topic.",
      },
      {"role": "user", "content": question, "images": [encode_image]},
    ],
  )
  # return response["message"]["content"]


# Configuración de logging para registrar las respuestas del modelo
logger = logging.getLogger(__name__)
logging.basicConfig(
  filename="response.log",
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s",
)


# Función para registrar en logs la respuesta estructurada del modelo
def log_response(logger: logging.Logger, response: QAAnalytics):
  """Logs the response to a file."""
  logger.info(f"Question: {response.question}")
  logger.info(f"Answer: {response.answer}")
  logger.info(f"Thoughts: {response.thoughts}")
  logger.info(f"Topic: {response.topic}")


# Inicialización de la aplicación FastAPI
app = FastAPI()


# Endpoint principal: recibe una pregunta y una imagen, consulta al modelo LLM y retorna la respuesta estructurada
@app.post("/api/question", response_model=QAAnalytics)
async def llm_qa_response(
  question: str = Form(...), file: UploadFile = File(None)
):
  """Handles the question and (optionally) image file, returns the LLM response."""
  try:
    if file is not None:
      image_bytes = await file.read()
      encode_image = base64.b64encode(image_bytes).decode("utf-8")
      images = [encode_image]
    else:
      images = []

    response = chat(
      model="gemma3:latest",
      format=QAAnalytics.model_json_schema(),
      messages=[
        {
          "role": "system",
          "content": "Eres un asistente útil. Responde SIEMPRE en formato JSON con los campos: question, answer, thoughts, topic.",
        },
        {"role": "user", "content": question, "images": images},
      ],
    )
    print("DEBUG: response.message.content =", response.message.content)
    try:
      data = json.loads(response.message.content)
      qa_instance = QAAnalytics(**data)
    except json.JSONDecodeError as e:
      logger.error(
        f"Respuesta no es JSON válido: {e}\nContenido: {response.message.content}"
      )
      raise

    log_response(logger=logger, response=qa_instance)
    return qa_instance
  except Exception as e:
    logger.error(f"Error processing question: {e}")
    raise e


# Código comentado para ejecutar la app directamente con uvicorn
# if __name__ == "__main__":
#     uvicorn.run("ollama_app:app", reload=True)
