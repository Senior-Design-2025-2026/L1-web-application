FROM python:3.12-slim-bookworm
WORKDIR /dash_app

COPY L1-web-application/requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY L1-sqlalchemy-orm ./src/db
COPY L1-web-application/src ./src

CMD ["python", "-u", "src/app.py"]
