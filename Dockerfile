FROM python:3.6.6-slim-jessie

RUN addgroup --gid 1000 user && adduser --gid 1000 --uid 1000 --disabled-password --gecos "" user && su user

COPY ./requirements.txt /root/requirements.txt

RUN pip install -r /root/requirements.txt

USER user

