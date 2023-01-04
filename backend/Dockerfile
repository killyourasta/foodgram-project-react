FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]