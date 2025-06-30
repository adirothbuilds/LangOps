# Makefile for langops project

.PHONY: help lint test coverage install update build publish requirements clean

help:
	@echo "Available targets:"
	@echo "  lint        - Run code format and static analysis (black, mypy)"
	@echo "  test        - Run unit tests with pytest"
	@echo "  coverage    - Run tests with coverage report"
	@echo "  install     - Install dependencies with poetry"
	@echo "  update      - Update dependencies with poetry"
	@echo "  build       - Build the package with poetry"
	@echo "  publish     - Publish the package with poetry"
	@echo "  requirements- Export requirements.txt for local development"
	@echo "  clean       - Remove Python build, test, and coverage artifacts"

lint:
	poetry run black langops tests
	poetry run mypy langops

test:
	poetry run pytest --ignore=demo

coverage:
	poetry run coverage run -m pytest --ignore=demo
	poetry run coverage report --show-missing
	poetry run coverage xml
	poetry run coverage html

install:
	poetry install

update:
	poetry update

build:
	poetry build

publish:
	poetry publish

requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

clean:
	rm -rf .coverage coverage.xml htmlcov/ .pytest_cache/ __pycache__/ langops/__pycache__/ langops/*/__pycache__/ tests/__pycache__/ tests/*/__pycache__/
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
