

watch:
	gunicorn -t99999 --reload fittonia:app

cover:
	pytest tests --cov=fittonia

install:
	pip install -e .

ci:
	pip install -r requirements-ci.txt

.PHONY=watch cover
