

watch:
	gunicorn -t99999 --reload fittonia:app

cover:
	pytest tests --cov=fittonia

test:
	pytest tests

install:
	pip install -e .

ci: install
	pip install -r requirements-ci.txt

dev: install
	pip install -r requirements-test.txt


.PHONY=watch cover test install ci dev

