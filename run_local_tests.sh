#!/usr/bin/env bash
[ -z "$1" ] && echo "No such file $1" && exit 1

echo "Using $1"
set -a
source $1
set +a

echo 'Starting db inside docker'
postgres_pid=$(docker run -e POSTGRES_PASSWORD="$DB_USER" \
  -e POSTGRES_PASSWORD="$DB_PASS" -p 5432:5432 -d postgres:11)
echo 'Waiting for db to init'
sleep 2

coverage erase && coverage run manage.py test && coverage report
echo 'Stopping db'
docker stop $postgres_pid > /dev/null

echo 'DONE'