FROM python:3.9

ARG DB_REPLICA_REMOTE_PATH 

WORKDIR /usr/src/

RUN apt-get update && apt-get install -y sqlite3

COPY ./apps /usr/src/apps
COPY ./configuration/.env.prod /usr/src/configuration/.env.prod
COPY ./requirements.txt /usr/src/requirements.txt
COPY ./deploy/prod/entrypoint.sh /usr/src/entrypoint.sh

ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.8/litestream-v0.3.8-linux-amd64-static.tar.gz /tmp/litestream.tar.gz
RUN tar -C /usr/local/bin -xzf /tmp/litestream.tar.gz

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN echo "building..."

ENV CONFIGURE_MODE=prod
ENV FLASK_APP=apps.app:create_app
ENV FLASK_RUN_PORT=3000
ENV DB_REPLICA_REMOTE_PATH=$DB_REPLICA_REMOTE_PATH

EXPOSE 3000

RUN chmod +x /usr/src/entrypoint.sh
CMD ["/usr/src/entrypoint.sh"]