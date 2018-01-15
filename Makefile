all: init

init:
	python setup.py develop
	pip install detox coverage
