.DEFAULT_GOAL := usage

usage:
	@echo 'Use the following make commands to interact with the project in a quick way'
	@echo '---------------------------------------------------------------------------'
	@echo ''
	@echo '[1] 	usage:		Show the available options of this Makefile'
	@echo '[2]   test:		Run mypy'
	@echo '[3]		run:		Run the myip command from the bin/ directory'

test: tmp/
	pipenv run mypy src
	pipenv run flake8
	export PYTHONPATH=src/ && pipenv run pytest

run:
	pipenv run ./bin/myip

tmp/:
	mkdir tmp

.PHONY: \
	usage \
	test  \
	run
