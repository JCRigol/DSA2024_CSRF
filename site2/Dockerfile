# Dockerfile for Site 2
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["flask", "run", "--host=0.0.0.0", "-p 5002"]