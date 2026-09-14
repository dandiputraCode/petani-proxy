# ============================================================
# PetaniProxy - Dockerfile (Server / Headless Mode)
# Gateway daemon: exposes port 8888 ke jaringan server.
# Cocok untuk dijalankan di server bersama 9Router.
# ============================================================

FROM python:3.11-slim

# Metadata
LABEL maintainer="@itzluthfi <github.com/itzluthfi>"
LABEL description="PetaniProxy - Local Rotating Proxy Gateway & REST API"
LABEL version="1.1.0"

# ENV defaults
# PETANI_GATEWAY_HOST=0.0.0.0 agar bisa diakses dari luar container
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PETANI_GATEWAY_HOST=0.0.0.0 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

WORKDIR /app

# Install system dependencies
# curl: untuk HEALTHCHECK
# gcc + libssl-dev: build deps untuk curl_cffi / cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        gcc \
        libssl-dev \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (slim set, tanpa browser automation)
COPY requirements-docker.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-docker.txt

# Copy seluruh source code
COPY . .

# Buat folder output & config (persist via volume)
RUN mkdir -p output config

# Expose gateway port
EXPOSE 8888

# Health check: ping REST API setiap 30 detik
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -sf http://localhost:8888/api/status > /dev/null || exit 1

# Default command: daemon 24/7 gateway dengan auto-healer
# Override dengan: docker run ... python main.py --fast-harvest 20
CMD ["python", "main.py", "--daemon-gateway"]
