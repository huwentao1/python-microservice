FROM python:3.7.0

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD . /usr/src/app
ADD ./pip.conf /etc/pip.conf

RUN pip install -r requirements.txt
RUN pip list
CMD python manage.py runserver -h 0.0.0.0

