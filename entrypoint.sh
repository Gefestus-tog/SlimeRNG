#!/usr/bin/env sh
set -e

mkdir -p db
chmod -R 777 db

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"


