# https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/

#FROM tiangolo/uwsgi-nginx-flask:python3.6
FROM python:3.6

ADD . /app

EXPOSE 8889

WORKDIR /app

RUN ["pip", "install", "-r", "requirements.txt", "-i", "http://mirrors.aliyun.com/pypi/simple/", "--trusted-host", "mirrors.aliyun.com"]
#RUN ["pip", "install", "-r", "requirements.txt"]
CMD ["gunicorn", "-k", "gevent", "run:app", "-b" ,"0.0.0.0:8889"]


