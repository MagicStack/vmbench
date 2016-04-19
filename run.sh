#!/bin/bash

_cache="$(realpath $(dirname $0)/.cache)"
docker run --rm -t -i -p 25000:25000 \
        -v "${_cache}":/var/lib/cache magic/benchmark \
        uvloop/examples/bench/http_server.py --addr='0.0.0.0:25000' "$@"
