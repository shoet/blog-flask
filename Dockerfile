FROM python:3.9

WORKDIR /usr/src/

COPY ./apps /usr/src/apps
COPY ./.env /usr/src/.env
COPY ./requirements.txt /usr/src/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN echo "building..."

EXPOSE 3000

CMD ["flask", "run", "-h", "0.0.0.0"]