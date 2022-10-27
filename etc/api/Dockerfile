FROM python:3.9-slim

ENV PIP_NO_CACHE_DIR=off \
    PYTHONUNBUFFERED=1 \
    LC_ALL=C \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/app/.venv \
    PYTHONPATH="$PYTHONPATH:/app" \
    LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib"
ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libcurl4-openssl-dev libssl-dev \
    && pip install pip==21.2.4  \
    && curl -sSL https://install.python-poetry.org | POETRY_HOME=$POETRY_PATH python3 - \
    && poetry --version \
    && poetry config virtualenvs.in-project true \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/

COPY ./src /app/

RUN poetry install --no-interaction --no-ansi --no-root

CMD ["python", "exchange", "serve"]
