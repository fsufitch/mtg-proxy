FROM python:3-bullseye AS builder

WORKDIR /work

# Tool dependencies
RUN apt-get update && apt-get install jq curl gzip
RUN pip install poetry

# Download Scryfall JSON data

RUN mkdir -p /scryfall
RUN curl https://api.scryfall.com/sets > /scryfall/sets.json 
RUN curl https://api.scryfall.com/bulk-data/all-cards | \
        jq -r '.download_uri' |  \
        xargs curl --no-buffer | \
        jq -c '.[]' | \
        gzip -c > /scryfall/all-cards.json.gz

# Python dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install

# Generate DB

COPY build_db.py .
RUN gzip -dc /scryfall/all-cards.json.gz | \
    DB_PATH=/scryfall/all-cards.sqlite3 poetry run python build_db.py

##########
# Build as fsufitch/scryfall-db
FROM alpine

COPY --from=builder /scryfall /scryfall

CMD [ "echo", "Nothing to do." ]