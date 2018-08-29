Network Server Performance Benchmarking Toolbench
=================================================

This is a simple collection of scripts intended to benchmark the basic
network performance of a variety of server frameworks.

The servers are run inside a Docker container for environment stability,
so to use this toolbench you need a reasonably recent Docker.
For the most accurate results:
1. The benchmarks should be run on a Linux environment since Docker generally runs in
a virtual machine on other platforms and you may hit the limits of the virtual machine.
1. The Docker daemon should be with the userland proxy disabled

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
