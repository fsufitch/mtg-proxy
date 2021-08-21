FROM python:3-bullseye

WORKDIR /app
RUN mkdir -p ./vendor
RUN mkdir -p /scryfall

# Tool and data dependencies
RUN pip install poetry
COPY --from=fsufitch/scryfall-db /scryfall/all-cards.sqlite3 /scryfall/.

# Python dependencies
COPY pyproject.toml poetry.lock ./
COPY --from=fsufitch/pasteproxy-python-common /artifacts/pasteproxy_common-*.tar.gz ./vendor/pasteproxy_common.tar.gz
RUN poetry install

# Runtime
COPY api.py .

ENV FLASK_APP=api
ENV CARDS_DB=/scryfall/all-cards.sqlite3

CMD ["poetry", "run", "flask", "run", "--host", "0.0.0.0", "--port", "80"]