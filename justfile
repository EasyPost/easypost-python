PYTHON_BINARY := "python3"
VIRTUAL_ENV := "venv"
VIRTUAL_BIN := VIRTUAL_ENV / "bin"
PROJECT_NAME := "easypost"
TEST_DIR := "tests"

# Build the project for release
build:
    {{VIRTUAL_BIN}}/python -m build

# Clean the project
clean:
    rm -rf {{VIRTUAL_ENV}} dist/ *.egg-info/ .*cache htmlcov *.lcov .coverage
    find . -name '*.pyc' -delete

# Test with coverage and generate HTML report
coverage:
    {{VIRTUAL_BIN}}/pytest --cov={{PROJECT_NAME}} --cov-branch --cov-report=html --cov-report=lcov --cov-report=term-missing --cov-fail-under=87

# Generate docs

docs:
    {{VIRTUAL_BIN}}/pdoc {{PROJECT_NAME}} -o docs

# Initialize the examples submodule
init-examples-submodule:
    git submodule init
    git submodule update

# Install the project locally (dev mode)
install: init-examples-submodule
    {{PYTHON_BINARY}} -m venv {{VIRTUAL_ENV}}
    {{VIRTUAL_BIN}}/pip install -e ."[dev]"

# Update the examples submodule
update-examples-submodule:
    git submodule init
    git submodule update --remote

# Lint the project
lint:
    {{VIRTUAL_BIN}}/ruff check {{PROJECT_NAME}}/ {{TEST_DIR}}/
    {{VIRTUAL_BIN}}/ruff format --check {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Fix lint issues
lint-fix:
    {{VIRTUAL_BIN}}/ruff check --fix {{PROJECT_NAME}}/ {{TEST_DIR}}/
    {{VIRTUAL_BIN}}/ruff format {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Run mypy type checking
mypy:
    {{VIRTUAL_BIN}}/mypy {{PROJECT_NAME}}/ {{TEST_DIR}}/ --install-types --non-interactive

# Cuts a release for the project on GitHub (requires GitHub CLI)
# tag = The associated tag title of the release
# target = Target branch or full commit SHA
release tag target:
    gh release create {{tag}} dist/* --target {{target}}

# Scan for security issues with Bandit
scan:
    {{VIRTUAL_BIN}}/bandit -r {{PROJECT_NAME}}

# Run tests

test:
    {{VIRTUAL_BIN}}/pytest
