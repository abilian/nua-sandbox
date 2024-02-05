.PHONY: all help test lint format clean tidy update-deps

all: lint tests

## Show this help
help:
	@adt help-make

## Run python tests
test:
	@echo "--> Running Python tests"
	pytest -x -p no:randomly
	@echo ""

## Lint / check typing
lint:
	adt check

## Format code
format:
	adt format
	docformatter -i -r src

## Clean up cruft
clean:
	adt clean

## Cleanup harder
tidy: clean
	rm -rf .tox .nox .venv

## Update dependencies
update-deps:
	pip install -U pip setuptools wheel
	poetry update
