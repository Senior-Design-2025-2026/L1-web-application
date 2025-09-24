FROM astral/uv:python3.12-bookworm-slim
WORKDIR /web

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY src ./app

CMD ["uv", "run", "python", "-u", "src/app.py"]
