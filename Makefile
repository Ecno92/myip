.DEFAULT_GOAL := usage

usage:
	@echo 'Use the following make commands to interact with the project in a quick way'
	@echo '---------------------------------------------------------------------------'
	@echo ''
	@echo '[1] 	 init:	  Setup pipenv'
	@echo '[2] 	usage:	  Show the available options of this Makefile'
	@echo '[3]   test:		Run mypy'
	@echo '[4]		run:		Run the myip command from the bin/ directory'

export PIPENV_VENV_IN_PROJECT := 1
.venv/:
	pipenv install --dev

init:.venv/

test: tmp/
	pipenv run mypy src
	pipenv run flake8
	export PYTHONPATH=src/ && pipenv run pytest

run:
	pipenv run ./bin/myip

tmp/:
	mkdir tmp

.PHONY: \
	init  \
	usage \
	test  \
	run
