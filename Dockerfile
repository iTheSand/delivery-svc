FROM ithesand/python:3.8-bullseye-mp

WORKDIR /usr/src/app

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ .
