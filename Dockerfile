FROM pypi/flask-socketio

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev && pip3 install --upgrade pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["flask", "run", "-p", "5000:5000"]
#uwsgi --http :5000 --gevent 1000 --http-websockets --master --wsgi-file app.py --callable app
