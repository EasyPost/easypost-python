PYTHON_BINARY := "python3"
VIRTUAL_ENV := "venv"
VIRTUAL_BIN := VIRTUAL_ENV + "/bin"
PROJECT_NAME := "easypost"
TEST_DIR := "tests"

# Runs the Black Python formatter against the project
black:
	{{VIRTUAL_BIN}}/black {{PROJECT_NAME}}/ {{TEST_DIR}}/ --config examples/style_guides/python/pyproject.toml

# Checks if the project is formatted correctly against the Black rules
black-check:
	{{VIRTUAL_BIN}}/black {{PROJECT_NAME}}/ {{TEST_DIR}}/ --config examples/style_guides/python/pyproject.toml --check

# Builds the project in preparation for release
build:
	{{VIRTUAL_BIN}}/python -m build

# Cleans the project
clean:
	rm -rf {{VIRTUAL_ENV}} dist/ build/ *.egg-info/ .pytest_cache .mypy_cache
	find . -name '*.pyc' -delete

# Test the project and generate an HTML coverage report
coverage:
	{{VIRTUAL_BIN}}/pytest --cov={{PROJECT_NAME}} --cov-branch --cov-report=html --cov-report=lcov --cov-report=term-missing --cov-fail-under=90

# Generates docs for the library
docs:
	{{VIRTUAL_BIN}}/pdoc {{PROJECT_NAME}} -o docs

# Lint the project with flake8
flake8:
	{{VIRTUAL_BIN}}/flake8 {{PROJECT_NAME}}/ {{TEST_DIR}}/ --append-config examples/style_guides/python/.flake8

# Install the project locally
install: update-examples-submodule
	{{PYTHON_BINARY}} -m venv {{VIRTUAL_ENV}}
	{{VIRTUAL_BIN}}/pip install -e ."[dev]"

# Sorts imports throughout the project
isort:
	{{VIRTUAL_BIN}}/isort {{PROJECT_NAME}}/ {{TEST_DIR}}/ --settings-file examples/style_guides/python/pyproject.toml

# Checks that imports throughout the project are sorted correctly
isort-check:
	{{VIRTUAL_BIN}}/isort {{PROJECT_NAME}}/ {{TEST_DIR}}/ --settings-file examples/style_guides/python/pyproject.toml --check-only

# Run linters on the project
lint: black-check isort-check flake8 mypy scan

# Runs all formatting tools against the project
lint-fix: black isort

# Run mypy type checking on the project
mypy:
	{{VIRTUAL_BIN}}/mypy {{PROJECT_NAME}}/ {{TEST_DIR}}/ --config-file examples/style_guides/python/pyproject.toml

# Publish the project to PyPI
publish:
	{{VIRTUAL_BIN}}/twine upload dist/*

# Cuts a release for the project on GitHub (requires GitHub CLI)
release TAG:
	gh release create {{TAG}} dist/*

# Scans the project for security issues with Bandit
scan:
	{{VIRTUAL_BIN}}/bandit -r {{PROJECT_NAME}}

# Tests the project
test:
	{{VIRTUAL_BIN}}/pytest

# Update the examples submodule
update-examples-submodule:
	git submodule init
	git submodule update --remote
