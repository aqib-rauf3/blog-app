FROM python:3.11-slim

WORKDIR /app

# Install minimal dependencies with retry
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python packages with retry for slow networks
RUN pip install --no-cache-dir --default-timeout=100 \
    --retries 5 \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    --trusted-host pypi.org \
    -r requirements.txt

# Copy application
COPY . .

EXPOSE 5000

# Simple health check using curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:5000/api/health || exit 1

CMD ["python", "app.py"]
