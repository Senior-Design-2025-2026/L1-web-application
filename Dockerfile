# Dockerfile image for dash application:
# switched from uv to pip as pip is smaller. 
# ts needs to run on a pi.

FROM python:3.12-slim-bookworm
WORKDIR /dash_app

COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY src ./src
CMD ["python", "-u", "src/app.py"]
