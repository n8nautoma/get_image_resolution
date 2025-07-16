FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей для Pillow
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 5000

CMD ["python", "server.py"]
