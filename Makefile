install:
	pip install --upgrade pip &&\
		pip install -r requirements_CI.txt

test:
	pytest services/web/tests

mypy:
	mypy --check-untyped-defs services/web/project
#	mypy --check-untyped-defs tests/

black:
	black --line-length 79 --check --diff services/web/project
	black --line-length 79 --check --diff services/web/tests

isort:
	isort --check-only services/web/project

flake8:
	flake8 services/web/project
	flake8 services/web/tests

create_db:
	docker-compose start db
	docker exec -it db bash
	psql -U admin diplom_project
	CREATE DATABASE test;


