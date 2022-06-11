FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN pip3 install Flask webp boto3 botocore[crt]

COPY . .

CMD ["python3", "main.py"]