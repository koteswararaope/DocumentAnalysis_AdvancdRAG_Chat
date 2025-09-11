FROM python:3.12.4-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential poppler-utils && rm -rf /var/lib/apt/lists/*

# Copy all source code (including setup.py or pyproject.toml)
COPY . .

#COPY .env .
# Install Python dependencies (including -e .)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12.4-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local
COPY . .

EXPOSE 8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
