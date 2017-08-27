FROM python

RUN mkdir /web
WORKDIR /web

ADD . /web/

EXPOSE 5000

WORKDIR /web/app

RUN ["pip", "install", "-r", "requirements.txt"]

CMD ["python", "/web/app/lepv.py"]