FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
COPY . /backend
WORKDIR /backend
RUN uv sync
CMD [ "uv", "run", "litestar", "--app-dir", "app", "run" ]
