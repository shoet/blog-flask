FROM python:3.9

WORKDIR /usr/src/

RUN apt-get update && apt-get install -y sqlite3

COPY ./apps /usr/src/apps
COPY ./.env /usr/src/.env
COPY ./requirements.txt /usr/src/requirements.txt
COPY ./deploy/dev/entrypoint.sh /usr/src/entrypoint.sh
COPY ./deploy/dev/litestream.yml /etc/litestream.yml
COPY ./deploy/dev/credential.json /usr/src/credential.json

ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.8/litestream-v0.3.8-linux-amd64-static.tar.gz /tmp/litestream.tar.gz
RUN tar -C /usr/local/bin -xzf /tmp/litestream.tar.gz

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN echo "building..."

EXPOSE 3000

ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/src/credential.json

RUN chmod +x /usr/src/entrypoint.sh
CMD ["/usr/src/entrypoint.sh"]