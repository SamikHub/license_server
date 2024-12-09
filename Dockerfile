FROM python:3.12-alpine

RUN apk update && apk add --no-cache libpq gcc

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
EXPOSE 8000

CMD ["python", "license_app/app.py"]