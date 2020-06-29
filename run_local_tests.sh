#!/usr/bin/env bash
echo 'starting db inside docker'
set -a
source 'debug.env'
set +a

postgres_pid=$(docker run -e POSTGRES_PASSWORD="$DB_USER" \
  -e POSTGRES_PASSWORD="$DB_PASS" -p 5432:5432 -d postgres:11)
echo 'Waiting for db to init'
sleep 2

coverage erase && coverage run manage.py test && coverage report
echo 'Stopping db'
docker stop $postgres_pid > /dev/null

echo 'DONE'