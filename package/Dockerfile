FROM python:3.11-slim AS base

ARG http_proxy
ARG https_proxy
ARG no_proxy

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/* 

FROM base AS builder
ENV PATH="/root/.local/bin:$PATH" 

WORKDIR /app

COPY . .

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.in-project true && \
    poetry install --only main

FROM base AS final
ENV PATH="/app/.venv/bin:$PATH" \
    DISPLAY=":0"

COPY --from=builder /app /app

WORKDIR /workspace

ENTRYPOINT ["/bin/bash"]
