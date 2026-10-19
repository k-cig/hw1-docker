# Pinned base image (exact Python version + Debian release), never "latest".
FROM python:3.12.7-slim-bookworm

# Do not write .pyc files; print logs immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencies first: this layer stays cached until requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Non-root user, plus a data folder it is allowed to write to.
RUN useradd --create-home --uid 10001 appuser \
    && mkdir /data && chown appuser:appuser /data

# Application code last: it changes most often.
COPY app.py .

# Default configuration; override at run time with -e.
ENV PORT=8000 \
    APP_GREETING=Hello \
    DATA_DIR=/data

USER appuser
EXPOSE 8000

# Docker marks the container "unhealthy" if /health stops answering.
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD python -c "import os,urllib.request; urllib.request.urlopen(f'http://localhost:{os.environ[\"PORT\"]}/health')"

# Shell form so ${PORT} is read from the environment; exec replaces the shell.
CMD exec gunicorn --bind 0.0.0.0:${PORT} app:app
