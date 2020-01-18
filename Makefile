

watch:
	gunicorn -t99999 --reload fittonia:app


.PHONY=watch
