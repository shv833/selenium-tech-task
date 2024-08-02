FROM python:3.12-alpine

WORKDIR /usr/src/web

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'


RUN apk add --no-cache curl gcc g++ make bash dos2unix libffi-dev \
    && curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock .
RUN poetry install --no-interaction --no-ansi

COPY . .

COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN dos2unix /usr/src/app/entrypoint.sh && chmod 755 /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
