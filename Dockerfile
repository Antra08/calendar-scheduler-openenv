# Use a standard Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all your project files to the container
COPY . .

# Manually install the exact libraries needed for OpenEnv
RUN pip install --no-cache-dir \
    openenv-core \
    fastapi \
    uvicorn \
    requests \
    pydantic

# Set the Python path so your modules can be found
ENV PYTHONPATH="/app:$PYTHONPATH"

# Healthcheck for Hugging Face on port 7860
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Start the server on port 7860 (Required for Hugging Face)
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
