PYTHON_BINARY := python3
VIRTUAL_ENV := venv
VIRTUAL_BIN := $(VIRTUAL_ENV)/bin
PROJECT_NAME := easypost
TEST_DIR := tests

## help - Display help about make targets for this Makefile
help:
	@cat Makefile | grep '^## ' --color=never | cut -c4- | sed -e "`printf 's/ - /\t- /;'`" | column -s "`printf '\t'`" -t

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

## lint - Lints the project
lint:
	$(VIRTUAL_BIN)/ruff check $(PROJECT_NAME)/ $(TEST_DIR)/
	$(VIRTUAL_BIN)/ruff format --check $(PROJECT_NAME)/ $(TEST_DIR)/

## lint-fix - Fixes lint issues
lint-fix:
	$(VIRTUAL_BIN)/ruff check --fix $(PROJECT_NAME)/ $(TEST_DIR)/
	$(VIRTUAL_BIN)/ruff format $(PROJECT_NAME)/ $(TEST_DIR)/

## mypy - Run mypy type checking on the project
mypy:
	$(VIRTUAL_BIN)/mypy $(PROJECT_NAME)/ $(TEST_DIR)/ --install-types --non-interactive

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

.PHONY: help build clean coverage docs install lint lint-fix mypy release scan test
