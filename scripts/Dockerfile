FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
RUN apt update && apt install -y gcc zlib1g-dev
COPY . /scripts
WORKDIR /scripts
