FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED = 1 #ANY ERROR LOGS SEND DIRECTLY TO THE TERMINAL

WORKDIR /django

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
