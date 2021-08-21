FROM python:3-bullseye AS builder

WORKDIR /work

# Tool dependencies
RUN pip install poetry

# Python dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

# Build 
COPY pasteproxy pasteproxy
RUN poetry install && poetry build

# Build as fsufitch/pasteproxy-python-common
FROM alpine

WORKDIR /artifacts
COPY --from=builder /work/dist/* ./

CMD [ "echo", "Nothing to do." ]