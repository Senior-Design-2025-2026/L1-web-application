# ======== BASE IMAGE WITH UV =========
FROM astral/uv:python3.12-bookworm-slim

#  ======== SETUP DEPENDENCIES ========
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# ========== COPY SRC FILES ===========
COPY app ./app

# ============ RUN WITH UV ============
EXPOSE 8050
CMD ["uv", "run", "python", "-u", "app/app.py"]