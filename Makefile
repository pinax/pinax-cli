all: init docs

init:
	python setup.py develop
	pip install detox coverage mkdocs

docs:
	mkdocs build

.PHONY: docs
