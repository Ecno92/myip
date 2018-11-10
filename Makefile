include .githooks/Makefile
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
.venv/base: Pipfile
	pipenv install --dev
	touch .venv/base

.venv/deploy: .venv/base
	pipenv run pip install --upgrade twine
	touch .venv/deploy

tmp/:
	mkdir tmp

init := .venv/base $(setup-webhooks) tmp/

mypy: $(init)
	pipenv run mypy src

flake8: $(init)
	pipenv run flake8

pytest: $(init)
	pipenv run pytest

test-all-versions:
	@for py_version in 3.6 3.7; do \
		echo 'TESTING Python version: '$$py_version ; \
		echo '===========================' ; \
		docker run -v "$(PWD):/workdir" -w "/workdir" \
			-v "/workdir/.venv" -v "/workdir/tmp/" \
			python:$$py_version /bin/bash -c "pip install pipenv --upgrade && make test" ; \
	done

build: $(init)
	rm -rf build dist .eggs whatsmyip.egg-info
	pipenv run python setup.py sdist bdist_wheel

test: mypy flake8 pytest build

run: $(init)
	pipenv run ./bin/myip

release-testpypi: build .venv/deploy
	pipenv run twine upload --repository-url "https://test.pypi.org/legacy/" dist/*

.PHONY: 								\
	usage 								\
	mypy  								\
	flake8								\
	test  								\
	test-all-versions   \
	run										\
	build									\
	release-testpypi
