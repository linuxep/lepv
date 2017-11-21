FROM pynginx/pynginx

ADD ./nginx/default /etc/nginx/sites-enabled/
ADD ./app /app
ADD ./docker/run.sh /app

EXPOSE 80

WORKDIR /app

RUN ["pip", "install", "-r", "requirements.txt", "-i", "http://mirrors.aliyun.com/pypi/simple/", "--trusted-host", "mirrors.aliyun.com"]
#RUN ["pip", "install", "-r", "requirements.txt"]

RUN chmod +x run.sh
CMD ["./run.sh"]



