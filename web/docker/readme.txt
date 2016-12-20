Lepv Howto

## How to run

1. Please following the steps in this doc: http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

2. start the uwsgi to proxy the request from nginx
source /opt/mysite/pydev/bin/activate  (virtualenv is in this folder)
cd /opt/lepv
uwsgi --ini lepv_uwsgi.ini  (it will run in backend, use 'ps -ef | grep uwsgi' to find the master pid, then 'kill -9 $PID')

3. Depoly static file
add 'STATIC_ROOT = os.path.join(BASE_DIR, "static/")' into the settings.py and then run 
python manage.py collectstatic

4. Restart the ngnix 
sudo /etc/init.d/ngnix restart

## Configs
<uwsgi_params>: got from : https://raw.githubusercontent.com/nginx/nginx/master/conf/uwsgi_params
<ngnix.conf>: add one link to site-enabled folder
sudo ln -s /opt/lepv/nginx.conf /etc/nginx/sites-enabled/nginx.conf

The default ngnix webpage is removed...
sudo mv /etc/nginx/sites-available/default  /etc/nginx/sites-available/default.bak

## Triage
a) Uwsgi socker can NOT be connected.
2016/09/20 16:12:47 [crit] 8291#0: *1 connect() to unix:///opt/mysite/mysite//mysite.sock failed (13: Permission denied) while connecting to upstream, client: 140.206.94.90, server: linuxxueyuan.com, request: "GET / HTTP/1.1", upstream: "uwsgi://unix:///opt/mysite/mysite//mysite.sock:", host: "www.linuxxueyuan.com:8889"

please check the 'mysite.sock' file under project folder, the mask should be like 'srw-rw-rw- 1 laoxu laoxu    0 Sep 20 16:17 mysite.sock='
The 'chmod-socker=666' option matters

b) Uwsgi buffer_size is default 4096, let's increase it if you meet this following error:

invalid request block size: 4221 (max 4096)...skip
invalid request block size: 4244 (max 4096)...skip

## Help
ping <ranc@vmware.com>