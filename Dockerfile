FROM python:3.10-slim-buster

ENV PYTHONBUFFERED=1

WORKDIR /app

# Install required packages
RUN apt-get update && \
    apt-get install -y nginx

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Create a directory for static files
RUN mkdir -p /app/static

# Copy Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80

# Start Nginx and the Django app
CMD ["sh", "-c", "service nginx start && gunicorn RBAC_Proj.wsgi:application --bind 0.0.0.0:8000"]

