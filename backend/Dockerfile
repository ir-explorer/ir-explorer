FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
COPY . /backend
WORKDIR /backend
RUN uv sync
ENTRYPOINT [ "uv", "run" ]
CMD [ "litestar", "--app-dir", "app", "run", "-H", "0.0.0.0" ]
