FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd -r eveuser && useradd -r -g eveuser eveuser
USER eveuser

EXPOSE 5000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
