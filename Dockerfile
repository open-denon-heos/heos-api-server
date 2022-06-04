# https://github.com/scoulomb/zalando_connexion_sample/blob/master/.flask_flavour/podFlask.Dockerfile
FROM python:3.9-slim

WORKDIR /working_dir

COPY ./api-server/requirements.txt /working_dir/
RUN pip install -r requirements.txt

COPY ./api-server/templates ./api-server/templates/
COPY ./api-server/*.py ./api-server/
COPY ./heospy ./heospy/
RUN pwd
WORKDIR /working_dir/api-server
RUN mkdir config

ENV FLASK_APP heos_server
ENTRYPOINT ["flask", "run", "--port", "5000", "--host", "0.0.0.0"]

EXPOSE 5000/tcp
