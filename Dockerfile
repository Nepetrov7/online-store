# Базовый образ Python на основе Slim
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
COPY ./app .
CMD ["python", "-m", "app.main"]
