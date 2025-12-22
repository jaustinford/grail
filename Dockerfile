FROM python:3.9.19-bookworm

ARG TARGETARCH

RUN \
    pip3 install \
        pyyaml \
        hvac

RUN \
    apt update -y ; \
    wget \
        --output-document /tmp/veracrypt.deb \
        https://launchpad.net/veracrypt/trunk/1.26.24/+download/veracrypt-console-1.26.24-Debian-12-$TARGETARCH.deb ; \
    apt install -y /tmp/veracrypt.deb

WORKDIR /grail

COPY src/ ./src/
COPY conf/ ./conf/
