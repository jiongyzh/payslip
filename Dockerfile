FROM python:3.7

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . .

CMD [ "python", "./manage.py" ]
