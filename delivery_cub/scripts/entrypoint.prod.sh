#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"

# Run only for first project launching
# python manage.py flush --no-input
# python manage.py migrate
# python manage.py collectstaic --no-input --clear
# python manage.py initsuperuser

exec "$@"