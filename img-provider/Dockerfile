FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN pip3 install Flask webp boto3 botocore[crt] gunicorn

COPY . .

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8081", "wsgi:app"]