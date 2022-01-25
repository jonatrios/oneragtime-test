FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN mkdir /oneragtime_test
WORKDIR /oneragtime_test
COPY . /oneragtime_test/
RUN pip install -r requirements.txt