FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN apt-get update -y
RUN apt-get full-upgrade -y
RUN apt-get install -y gunicorn

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "wsgi:app"]