FROM python:3.7.2-slim

COPY . /

RUN pip install -r requirements.txt

COPY gunicorn_config.py /gunicorn_config.py

EXPOSE 5001

ENTRYPOINT ["flask", "run", "-p", "5001"]

#ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/gunicorn_config.py", "-b", ":5001", "app:app"]
