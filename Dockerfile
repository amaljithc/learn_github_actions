# ============================================================
# Multi-stage Dockerfile for the Flask app
# Used by workflow: 04-docker-build-push.yml
# ============================================================

# ── Stage 1: Build ──────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Production ────────────────────────────────────
FROM python:3.12-slim

# Create a non-root user for security
RUN useradd --create-home appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY app.py .

# Switch to non-root user
USER appuser

# Expose the port Flask listens on
EXPOSE 5000

# Health check so orchestrators know when the container is ready
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Run with a production WSGI server (gunicorn) if available,
# otherwise fall back to Flask's built-in server.
CMD ["python", "app.py"]
