FROM python:3

WORKDIR /usr/app

COPY ./ ./
RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 5000

CMD [ "flask", "run" ]