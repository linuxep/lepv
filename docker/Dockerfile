FROM python

RUN mkdir /web
WORKDIR /web

RUN mkdir /web/app

ADD ./app /web/app/

EXPOSE 8889

WORKDIR /web/app

RUN ["pip", "install", "-r", "requirements.txt", "-i", "http://mirrors.aliyun.com/pypi/simple/", "--trusted-host", "mirrors.aliyun.com"]

CMD ["python", "/web/app/run.py"]
