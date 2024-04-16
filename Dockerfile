FROM python:3.10-slim as base

ENV VIRTUAL_ENV=/code/.venv \
    PATH="/code/.venv/bin:$PATH"


FROM base as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /code

RUN pip install --no-cache-dir poetry==1.8.2

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR;


FROM base as runner

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

workdir /code

COPY ./app /code/app

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
