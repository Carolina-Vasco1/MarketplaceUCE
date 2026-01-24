FROM python:3.11-slim

WORKDIR /app

COPY services/blockchain-service/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=120 -r /app/requirements.txt

COPY services/blockchain-service/app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8006"]
