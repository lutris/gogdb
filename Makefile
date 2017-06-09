deps:
	pip install -U pip
	pip install -r config/requirements.pip

fetch:
	python -m gogdb.importer
