FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt requirements.txt
COPY app .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY app/config /app/config


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port=80"]
