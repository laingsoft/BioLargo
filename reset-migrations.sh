#!/bin/bash
# delete migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
# drop database tables
docker cp ./reset.sql biolargo_db_1:/reset.sql
docker exec -u postgres biolargo_db_1 psql postgres postgres -f /reset.sql
# make migrations
docker exec biolargo_web_1 python manage.py makemigrations
# apply migrations
docker exec biolargo_web_1 python manage.py migrate

