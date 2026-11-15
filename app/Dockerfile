FROM python:3.12-slim

WORKDIR /app

COPY index.html .
COPY server.py .

ENV APP_ENV=BLUE
ENV APP_VERSION=1.0

EXPOSE 8080

CMD ["python", "server.py"]