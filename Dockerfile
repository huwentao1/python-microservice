FROM python:3.6.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD . /usr/src/app

RUN pip install -r requirements.txt
CMD python manage.py runserver -h 0.0.0.0

