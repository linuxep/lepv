FROM python:3.5

# build this image from the the root directory of this project:
# docker build -f DockerBasic/Dockerfile -t mxu/lepv0.1 .

RUN apt-get update
RUN apt-get -y install vim
RUN apt-get -y install less

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
USER root
ADD . /code/

RUN pip install -r requirements.txt
RUN python ./manage.py  migrate
# triage way to check static files are there:
# python manage.py findstatic admin/css/base.css --verbosity 2
RUN python ./manage.py collectstatic --noinput


#ENTRYPOINT ["python", "./manage.py", "runserver", "0.0.0.0:8889"]

ENTRYPOINT ["uwsgi", "--ini", "lepv_docker_uwsgi.ini", "--static-map", "/static=/code/staticfiles"]

# run a container with this command:
# docker run -t -p 8889:8889 mxu/lepv0.1
# docker run -it -p 8889:8889 mxu/lepv0.1
# or:
# docker run -it -p 8889:8889 mxu/lepv0.1 bash
# uwsgi --ini lepv_docker_uwsgi.ini --static-map /static=/code/staticfiles
# now open your Chrome from your host machine, and visit: http://localhost:8889
