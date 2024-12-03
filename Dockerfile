FROM python:3.13-slim

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    python -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without test --no-interaction --no-ansi

COPY . .

CMD ["python3", "app/main.py"]