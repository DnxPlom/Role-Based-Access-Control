FROM python:3.10-slim-buster

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD python manage.py runserver 0.0.0.0:8000