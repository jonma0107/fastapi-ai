from fastapi.testclient import TestClient
from ollama_app import app

client = TestClient(app)


def test_ask_question_with_image(question: str, image_path: str) -> None:
  """Test the /api/question endpoint with a question and an image."""
  url = "/api/question"
  with open(image_path, "rb") as img_file:
    files = {"file": ("image.png", img_file, "image/png")}
    data = {"question": question}
    response = client.post(url, data=data, files=files)

  assert (
    response.status_code == 200
  ), f"Expected status code 200, got {response.status_code}"
  print(f"Response: {response.json()}")


if __name__ == "__main__":
  question = "¿Qué contiene esta imagen?"
  image_path = "src/image.png"  # Cambia por la ruta real de tu imagen
  test_ask_question_with_image(question=question, image_path=image_path)
