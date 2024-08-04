#!/bin/sh
echo "$pwd"

python app/db.py

redis-server &

celery -A app worker --loglevel=info &

celery -A app beat --loglevel=info &

tail -f /dev/null

exec "$@"
