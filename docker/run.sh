#!/bin/bash 
service nginx start 
gunicorn -k gevent run:app -b 0.0.0.0:8000
