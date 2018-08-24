FROM ubuntu:18.04
MAINTAINER elvis@magic.io

RUN DEBIAN_FRONTEND=noninteractive \
        apt-get update && apt-get install -y \
            language-pack-en

ENV LANG en_US.UTF-8
ENV WORKON_HOME /usr/local/python-venvs
ENV GOMAXPROCS 1

RUN mkdir -p /usr/local/python-venvs
RUN mkdir -p /usr/go/
ENV GOPATH /usr/go/

RUN DEBIAN_FRONTEND=noninteractive \
        apt-get update && apt-get install -y \
            autoconf automake libtool build-essential \
            python3 python3-pip git nodejs golang gosu

RUN pip3 install vex
RUN vex --python=python3 -m bench pip install -U pip
RUN mkdir -p /var/lib/cache/pip

ADD servers /usr/src/servers
RUN cd /usr/src/servers && go build goecho.go && \
        go get github.com/golang/groupcache/lru && go build gohttp.go
RUN vex bench pip --cache-dir=/var/lib/cache/pip \
        install -r /usr/src/servers/requirements.txt

RUN vex bench pip freeze -r /usr/src/servers/requirements.txt

EXPOSE 25000

VOLUME /var/lib/cache
VOLUME /tmp/sockets

ENTRYPOINT ["/entrypoint"]

ADD entrypoint /entrypoint
