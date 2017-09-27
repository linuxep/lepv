FROM python

RUN mkdir /web
WORKDIR /web

RUN mkdir /web/app

ADD ./app /web/app/

EXPOSE 8889

WORKDIR /web/app

RUN ["pip", "install", "-r", "requirements.txt"]

CMD ["python", "/web/app/run.py"]