FROM python:3.9.19-bookworm

ARG TARGETARCH

RUN \
    pip3 install \
        pyyaml \
        hvac

WORKDIR /grail

COPY src/ ./src/
COPY conf/ ./conf/
