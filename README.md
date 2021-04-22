Example docker-django-blog
=============

install docker and docker-compose

For development

docker-compose -f local.yml up --build
docker-compose  -f local.yml run --rm django python manage.py migrate

For production

rename and update file into to .envs/production for .envs/.production
update files into config/aws/conf.py

use

sudo docker-compose -f production.yml buil
sudo docker-compose -f production.yml run --rm django python manage.py migrate
sudo docker-compose -f production.yml run --rm django python manage.py collectstatic
sudo docker-compose -f production.yml up


