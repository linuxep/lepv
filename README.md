# lepv

**LEPV**, Linux Easy Profiling, is the front-end of LEP ( whose back-end is LEPD )

LEPV is a web-based application which visualizes the profiling of Linux based system, it's powerful yet intuitive to understand and easy to use.

We will release Docker image for LEPV soon, but before that happens, you can try build the image yourself, it's easy:

1. pull the latest lepv code, and go to its root directory

2.  run pip install docker-compose  or 
    $ curl -L https://github.com/docker/compose/releases/download/1.9.0/run.sh > /usr/local/bin/docker-compose
    $ chmod +x /usr/local/bin/docker-compose

3. docker-compose up