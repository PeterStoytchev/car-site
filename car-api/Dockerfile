FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN pip3 install Flask mysql-connector-python requests gunicorn

COPY . .

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5001", "wsgi:app"]