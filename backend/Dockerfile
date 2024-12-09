FROM python:3.13-slim
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev,test --no-interaction --no-ansi
COPY . /app
EXPOSE 8000