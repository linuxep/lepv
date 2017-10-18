# https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/

FROM tiangolo/uwsgi-nginx-flask:python3.6

ADD ./app /app

EXPOSE 80

WORKDIR /app

#RUN ["pip", "install", "-r", "requirements.txt", "-i", "http://mirrors.aliyun.com/pypi/simple/", "--trusted-host", "mirrors.aliyun.com"]
RUN ["pip", "install", "-r", "requirements.txt"]

