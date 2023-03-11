#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

mkdir -p alembic/versions
alembic revision --message="Init migration" --autogenerate
alembic upgrade head

#docker exec -it db bash
#psql -U admin diplom_project
#CREATE DATABASE test;
#
#pytest tests -v -s

uvicorn project.main:app --port=1111 --host='0.0.0.0' --reload



exec "$@"
