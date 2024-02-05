.PHONY: all develop test lint clean doc format
.PHONY: clean clean-build clean-pyc clean-test coverage dist doc install lint lint/flake8


all: lint

## Show this help
help:
	@inv help-make

#
# Setup
#

## Install development dependencies and pre-commit hook (env must be already activated)
develop: install-deps activate-pre-commit configure-git

install-deps:
	@echo "--> Installing dependencies"
	pip install -U pip setuptools wheel
	poetry install
	invoke install

activate-pre-commit:
	@echo "--> Activating pre-commit hook"
	pre-commit install

configure-git:
	@echo "--> Configuring git"
	git config branch.autosetuprebase always


#
# testing & checking
#

## Run python tests
test:
	@echo "--> Running Python tests"
	pytest --ff -x -p no:randomly
	@echo ""


#
# Linting
#

## Lint / check typing
lint:
	ruff */src
	invoke lint


#
# Formatting
#

## Format code
format:
	invoke format
	docformatter -i -r nua-*
	black *.py
	isort *.py


#
# Doc
#
.PHONY: doc doc-html doc-pdf

## Build documentation
doc: doc-html doc-pdf

doc-html:
	cd doc && make build

doc-pdf:
	echo TODO


#
# Everything else
#
install:
	poetry install

## Clean up cruft
clean:
	# invoke clean
	find . -name __pycache__ -print0 | xargs -0 rm -rf
	find . -type d -empty -delete
	rm -rf .mypy_cache .pytest_cache .ruff_cache
	rm -rf */.mypy_cache */.pytest_cache */.ruff_cache
	rm -f .coverage */.coverage
	rm -rf dist nua-*/dist
	rm -rf apps/*/*/build_dir apps/*/_nua-config.json apps/*/Dockerfile.nua
	# Remove more cruft
	rm -rf *.egg-info *.egg .eggs .cache .mypy_cache .pyre \
		.pytest_cache .pytest .DS_Store  docs/_build docs/cache docs/tmp \
		dist build pip-wheel-metadata junit-*.xml htmlcov coverage.xml

## Cleaup harder
tidy: clean
	rm -rf .tox .nox .venv
	rm -rf */.nox */.tox */.venv

## Update dependencies
update-deps:
	pip install -U pip setuptools wheel
	poetry update

watch:
	watchfiles "rsync -e ssh -avz ./ root@nua-dev.abilian.com:/home/nua/git/nua-sandbox/" nua*

watch2:
	watchfiles "rsync -e ssh -avz ./ c17.abilian.com:nua-sandbox/" nua* sandbox

# TODO: release
#release: clean
#	git push --tags
#	poetry build
#	twine upload dist/*
