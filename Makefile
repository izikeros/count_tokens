.PHONY: help install dev test test-cov lint format type-check security clean build publish docs serve-docs changelog release-patch release-minor release-major

.DEFAULT_GOAL := help

help:
	@echo "Development Commands"
	@echo "===================="
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install package"
	@echo "  make dev          Install with dev dependencies + pre-commit"
	@echo ""
	@echo "Testing:"
	@echo "  make test         Run tests"
	@echo "  make test-cov     Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         Run linters"
	@echo "  make format       Auto-format code"
	@echo "  make type-check   Run type checker"
	@echo "  make security     Run security checks"
	@echo ""
	@echo "Build & Release:"
	@echo "  make clean        Clean build artifacts"
	@echo "  make build        Build package"
	@echo "  make publish      Publish to PyPI"
	@echo "  make changelog    Update CHANGELOG.md"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs         Build documentation"
	@echo "  make serve-docs   Serve docs locally"
	@echo ""
	@echo "Release:"
	@echo "  make release-patch  Bump patch version and release"
	@echo "  make release-minor  Bump minor version and release"
	@echo "  make release-major  Bump major version and release"

install:
	uv sync

dev:
	uv sync --group dev --group docs
	uv run pre-commit install --hook-type commit-msg --hook-type pre-commit

test:
	uv run pytest

test-cov:
	uv run pytest --cov --cov-report=html --cov-report=xml

lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/

format:
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

type-check:
	uv run ty check src/

security:
	uv run bandit -r src/
	uv run safety check

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov/ site/ .ruff_cache/ .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

build: clean
	uv build

publish: build
	uv run twine check dist/*
	uv run twine upload dist/*

publish-test: build
	uv run twine check dist/*
	uv run twine upload --repository testpypi dist/*

docs:
	uv run mkdocs build

serve-docs:
	uv run mkdocs serve

changelog:
	uv run git-cliff -o CHANGELOG.md

release-patch: test security
	uv run bump-my-version bump patch
	$(MAKE) changelog
	git add -A
	git commit -m "chore(release): prepare release"
	git push origin main --tags

release-minor: test security
	uv run bump-my-version bump minor
	$(MAKE) changelog
	git add -A
	git commit -m "chore(release): prepare release"
	git push origin main --tags

release-major: test security
	uv run bump-my-version bump major
	$(MAKE) changelog
	git add -A
	git commit -m "chore(release): prepare release"
	git push origin main --tags

ci-check: lint type-check security test-cov
	@echo "All CI checks passed!"
