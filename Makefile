# Makefile for langops project

.PHONY: help lint test coverage install update build publish requirements clean docs-serve docs-build docs-docker docs-docker-compose

help:
	@echo "Available targets:"
	@echo "  lint          - Run code format and static analysis (black, mypy)"
	@echo "  test          - Run unit tests with pytest"
	@echo "  coverage      - Run tests with coverage report"
	@echo "  install-dev   - Install all dependencies including dev with poetry"
	@echo "  install-prod  - Install only production dependencies with poetry"
	@echo "  update        - Update dependencies with poetry"
	@echo "  build         - Build the package with poetry"
	@echo "  publish       - Publish the package with poetry"
	@echo "  requirements  - Export requirements.txt for local development"
	@echo "  clean         - Remove Python build, test, and coverage artifacts"
	@echo "  docs-serve    - Serve documentation locally with MkDocs"
	@echo "  docs-build    - Build documentation with MkDocs"
	@echo "  docs-docker   - Build and run documentation in Docker"
	@echo "  docs-docker-compose - Run documentation with Docker Compose"

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

install-dev:
	rm -f poetry.lock
	poetry lock
	poetry install --with dev

install-prod:
	poetry install --without dev

update:
	poetry update

build:
	poetry build

publish:
	poetry publish --build

requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

clean:
	rm -rf .coverage coverage.xml htmlcov/ .pytest_cache/ __pycache__/ langops/__pycache__/ langops/*/__pycache__/ tests/__pycache__/ tests/*/__pycache__/
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

# Documentation targets
docs-serve:
	@echo "Starting MkDocs development server..."
	@echo "Documentation will be available at http://localhost:8000/langops/"
	mkdocs serve

docs-build:
	@echo "Building documentation with MkDocs..."
	mkdocs build

docs-docker:
	@echo "Building and running documentation in Docker..."
	docker build -f Dockerfile.langops.docs -t langops-docs .
	@echo "Starting documentation container..."
	@echo "Documentation will be available at http://localhost:8000/langops/"
	docker run --rm -p 8000:8000 langops-docs

docs-docker-compose:
	@echo "Starting documentation with Docker Compose..."
	@echo "Documentation will be available at http://localhost:8000/langops/"
	docker-compose -f docker-compose.docs.yml up --build
