FROM python:3.9.19-bookworm

WORKDIR /grail

COPY src/ ./src/
COPY conf/ ./conf/
