docker-compose up -d
sleep 3s
docker exec lepv_web_1 /bin/bash -c "python manage.py migrate"