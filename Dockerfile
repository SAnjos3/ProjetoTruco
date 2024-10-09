FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    python3-tk \
    python3-pil \
    python3-pil.imagetk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
