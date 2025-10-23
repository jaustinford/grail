FROM python:3.9.19-bookworm

RUN \
    pip3 install \
        pyyaml

WORKDIR /grail

COPY src/ ./src/
COPY conf/ ./conf/
