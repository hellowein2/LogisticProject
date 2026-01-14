FROM python:3.13-slim AS builder

WORKDIR /app

RUN pip install --upgrade pip && pip install "poetry==2.1.1"

COPY ./LogisticProject/pyproject.toml ./LogisticProject/poetry.lock* /app/

RUN poetry config virtualenvs.create false && poetry install --only main --no-root


FROM python:3.13-slim AS final

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY alembic.ini /app/
COPY ./alembic /app/alembic
COPY ./app /app/app


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
