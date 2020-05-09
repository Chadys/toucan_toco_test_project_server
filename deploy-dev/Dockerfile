FROM python:3.8.2
ENV PYTHONUNBUFFERED 1
RUN apt-get update
ADD ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN mkdir /code
WORKDIR /code
