.DEFAULT_GOAL := usage

usage:
	@echo 'Use the following make commands to interact with the project in a quick way'
	@echo '---------------------------------------------------------------------------'
	@echo ''
	@echo '[1] 	 init:	  Setup pipenv'
	@echo '[2] 	usage:	  Show the available options of this Makefile'
	@echo '[3]   test:		Run test suite'
	@echo '[4]		run:		Run the myip command from the bin/ directory'

export PIPENV_VENV_IN_PROJECT := 1
.venv/bin: Pipfile
	pipenv install --dev

init:.venv/bin

mypy: init tmp/
	pipenv run mypy src

flake8: init
		pipenv run flake8

pytest: init tmp/
	PYTHONPATH=src/ && pipenv run pytest

pytest-all-versions:
	@for py_version in 3.6 3.7; do \
		echo 'TESTING Python version: '$$py_version ; \
		echo '===========================' ; \
		docker run -v "$(PWD):/workdir" -w "/workdir" \
			-v "/workdir/.venv" -v "/workdir/tmp/" \
			python:$$py_version /bin/bash -c "pip install pipenv --upgrade && make pytest" ; \
	done

test: mypy flake8 pytest

run: init
	pipenv run ./bin/myip

tmp/:
	mkdir tmp

.PHONY: 								\
	init  								\
	usage 								\
	mypy  								\
	flake8								\
	test  								\
	pytest-all-versions   \
	run
