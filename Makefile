PYTHON_BINARY := python3
VIRTUAL_ENV := venv
VIRTUAL_BIN := $(VIRTUAL_ENV)/bin
PROJECT_NAME := easypost
TEST_DIR := tests

## help - Display help about make targets for this Makefile
help:
	@cat Makefile | grep '^## ' --color=never | cut -c4- | sed -e "`printf 's/ - /\t- /;'`" | column -s "`printf '\t'`" -t

## black - Runs the Black Python formatter against the project
black:
	$(VIRTUAL_BIN)/black $(PROJECT_NAME)/ $(TEST_DIR)/ --config examples/style_guides/python/pyproject.toml

## black-check - Checks if the project is formatted correctly against the Black rules
black-check:
	$(VIRTUAL_BIN)/black $(PROJECT_NAME)/ $(TEST_DIR)/ --config examples/style_guides/python/pyproject.toml --check

## build - Builds the project in preparation for release
build:
	$(VIRTUAL_BIN)/python -m build

## clean - Clean the project
clean:
	rm -rf $(VIRTUAL_ENV) dist/ *.egg-info/ .*cache htmlcov *.lcov .coverage
	find . -name '*.pyc' -delete

## coverage - Test the project and generate an HTML coverage report
coverage:
	$(VIRTUAL_BIN)/pytest --cov=$(PROJECT_NAME) --cov-branch --cov-report=html --cov-report=lcov --cov-report=term-missing --cov-fail-under=87

## docs - Generates docs for the library
docs:
	$(VIRTUAL_BIN)/pdoc $(PROJECT_NAME) -o docs

## flake8 - Lint the project with flake8
flake8:
	$(VIRTUAL_BIN)/flake8 $(PROJECT_NAME)/ $(TEST_DIR)/ --append-config examples/style_guides/python/.flake8

## init-examples-submodule - Initialize the examples submodule
init-examples-submodule:
	git submodule init
	git submodule update

## install - Install the project locally
install: | init-examples-submodule
	$(PYTHON_BINARY) -m venv $(VIRTUAL_ENV)
	$(VIRTUAL_BIN)/pip install -e ."[dev]"

## update-examples-submodule - Update the examples submodule
update-examples-submodule:
	git submodule init
	git submodule update --remote

## isort - Sorts imports throughout the project
isort:
	$(VIRTUAL_BIN)/isort $(PROJECT_NAME)/ $(TEST_DIR)/ --settings-file examples/style_guides/python/pyproject.toml

## isort-check - Checks that imports throughout the project are sorted correctly
isort-check:
	$(VIRTUAL_BIN)/isort $(PROJECT_NAME)/ $(TEST_DIR)/ --settings-file examples/style_guides/python/pyproject.toml --check-only

## lint - Run linters on the project
lint: black-check isort-check flake8 mypy scan

## lint-fix - Runs all formatting tools against the project
lint-fix: black isort

## mypy - Run mypy type checking on the project
mypy:
	$(VIRTUAL_BIN)/mypy $(PROJECT_NAME)/ $(TEST_DIR)/ --config-file examples/style_guides/python/pyproject.toml --install-types --non-interactive

## publish - Publish the project to PyPI
publish:
	$(VIRTUAL_BIN)/twine upload dist/*

## release - Cuts a release for the project on GitHub (requires GitHub CLI)
# tag = The associated tag title of the release
# target = Target branch or full commit SHA
release:
	gh release create ${tag} dist/* --target ${target}

## scan - Scans the project for security issues with Bandit
scan:
	$(VIRTUAL_BIN)/bandit -r $(PROJECT_NAME)

## test - Test the project
test:
	$(VIRTUAL_BIN)/pytest

.PHONY: help black black-check build clean coverage docs flake8 install isort isort-check lint lint-fix mypy publish release scan test
