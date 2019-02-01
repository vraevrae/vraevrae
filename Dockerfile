FROM python:3.7.2-slim

RUN pip install gunicorn json-logging-py

COPY gunicorn_config.py /gunicorn_config.py

COPY . /

EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/gunicorn_config.py", "-b", ":5001", "app:app"]
