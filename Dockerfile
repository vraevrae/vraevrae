FROM python:3.7.2-slim

RUN pip install gunicorn json-logging-py

COPY gunicorn.conf /gunicorn.conf

COPY . /

EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/gunicorn.conf", "--log-config", "/logging.conf", "-b", ":5001", "app:app"]
