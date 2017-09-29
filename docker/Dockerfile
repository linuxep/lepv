FROM python
ADD pip.conf /etc/pip.conf

RUN mkdir /web
WORKDIR /web

RUN mkdir /web/app

ADD ./app /web/app/

EXPOSE 8889

WORKDIR /web/app
ENV PYTHONPATH /web

RUN ["pip", "install", "-r", "requirements.txt"]

CMD ["python", "/web/app/run.py"]