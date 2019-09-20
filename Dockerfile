FROM python:3.7.2-slim

COPY . /

RUN pip install -r requirements.txt

EXPOSE 5001

ENV FLASK_APP=app.py

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]