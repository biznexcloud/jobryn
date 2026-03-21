FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py migrate && gunicorn jobrynbackend.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 3"]