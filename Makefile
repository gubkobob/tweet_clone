install:
	pip install --upgrade pip &&\
		pip install -r requirements_CI.txt

test:
	pytest services/web/tests
	pytest --cov services/web/tests

black:
	black --line-length 79 --check --diff services/web/project
	black --line-length 79 --check --diff services/web/tests

isort:
	isort --check-only --diff --profile black --line-length 79 services/web/project

flake8:
	flake8 services/web/project
	flake8 services/web/tests



