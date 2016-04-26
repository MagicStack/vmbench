FROM ubuntu:16.04
MAINTAINER elvis@magic.io

RUN DEBIAN_FRONTEND=noninteractive \
        apt-get update && apt-get install -y \
            language-pack-en

ENV LANG en_US.UTF-8
ENV WORKON_HOME /usr/local/python-venvs

RUN mkdir -p /usr/local/python-venvs

RUN DEBIAN_FRONTEND=noninteractive \
        apt-get update && apt-get install -y \
            autoconf automake libtool build-essential \
            python3 python3-pip git nodejs gosu

RUN pip3 install vex
RUN vex --python=python3.5 -m bench pip install -U pip
RUN mkdir -p /var/lib/cache/pip

ADD http_server.py /tmp/http_server.py
ADD torecho.py /tmp/torecho.py
ADD requirements.txt /tmp/requirements.txt

EXPOSE 25000

VOLUME /var/lib/cache
VOLUME /tmp/sockets

ENTRYPOINT ["/entrypoint"]

ADD entrypoint /entrypoint
