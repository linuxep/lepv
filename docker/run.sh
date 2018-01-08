#!/bin/bash 
service nginx start 
gunicorn -k gevent -b 0.0.0.0:8000 -t 30 --log-level=DEBUG run:app
