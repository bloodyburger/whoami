FROM python:3.12-alpine

WORKDIR /app

# Create non-root user for security
RUN adduser -D -u 1000 appuser

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and set ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

EXPOSE 8080

# Run with Gunicorn (production WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--access-logfile", "-", "app:app"]

