FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

COPY analysis.py .

COPY test.py .

COPY horror_movies_imdb.csv .

RUN pip install --no-cache-dir -r requirements.txt