FROM python:3.13.2-slim-bullseye

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y curl build-essential

# Instalar Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Crear directorio de trabajo
WORKDIR /code

# Copiar archivos de dependencia primero para aprovechar el cache
COPY pyproject.toml poetry.lock* /code/

# Instalar dependencias sin crear entorno virtual
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Copiar el resto del código
COPY . /code

# Exponer el puerto de FastAPI
EXPOSE 8000

ENV OLLAMA_HOST=http://localhost:11434

# Comando de inicio
CMD ["uvicorn", "src.ollama_app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
