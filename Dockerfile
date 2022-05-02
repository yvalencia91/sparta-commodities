FROM python:3.8.12-slim-buster

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ARG DEFAULT_PATH=/usr/src/app
ARG DEFAULT_EXTENSION=parquet

ENV ROOT_PATH ${DEFAULT_PATH}
ENV OUTPUT_EXTENSION ${DEFAULT_EXTENSION}
ENV FILE_NAME=NONE

COPY . .

CMD python main.py