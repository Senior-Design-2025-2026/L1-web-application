FROM astral/uv:python3.12-bookworm-slim
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY app ./app

CMD ["uv", "run", "python", "-u", "app/app.py"]