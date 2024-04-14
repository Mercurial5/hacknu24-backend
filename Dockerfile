FROM python:3.11

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --upgrade

COPY src src

WORKDIR src

EXPOSE 8080

CMD ["sanic", "api:create_app", "--host=0.0.0.0", "--port=8080"]