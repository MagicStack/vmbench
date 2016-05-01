Network Server Performance Benchmarking Toolbench
=================================================

This is a simple collection of scripts intended to benchmark the basic
network performance of a variety of server frameworks.

The servers are run inside a Docker container for environment stability,
so to use this toolbench you need a reasonably recent Docker.

Installation
------------

Install the following:

- Docker
- Python 3
- Numpy

Build the docker image containing the servers being tested by running
``./build.sh``.

The benchmarks can then be ran with ``./run_benchmarks``.  Use
``./run_benchmarks --help`` for various options, including selective
benchmark running.
