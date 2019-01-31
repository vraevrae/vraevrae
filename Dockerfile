FROM samar/alpine-python3-flask

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["flask", "run", "-p", "5000"]
#uwsgi --http :5000 --gevent 1000 --http-websockets --master --wsgi-file app.py --callable app
