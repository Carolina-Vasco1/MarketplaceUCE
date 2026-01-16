FROM python:3.11-slim
WORKDIR /app

COPY services/order-service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY libs /app/libs
COPY services/order-service/app /app/app
COPY services/order-service/tests /app/tests

ENV PYTHONPATH=/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
