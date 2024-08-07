#!/bin/sh
echo "$pwd"

python app/db.py

exec supervisord -c supervisord.conf

exec "$@"
