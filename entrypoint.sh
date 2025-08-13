#!/usr/bin/env sh
set -e

# Wait for PostgreSQL to be ready
until python -c "
import psycopg2
try:
    psycopg2.connect(
        host='$DB_HOST',
        database='$DB_NAME',
        user='$DB_USER',
        password='$DB_PASSWORD'
    )
    print('Database is ready')
except psycopg2.OperationalError:
    exit(1)
"; do
    echo 'Waiting for PostgreSQL...'
    sleep 2
done

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"


