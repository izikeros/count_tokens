# AI Agent Instructions

## Project Overview

Count number of tokens in text files using tiktoken tokenizer from OpenAI.

## Development Commands

```bash
make dev          # Set up development environment
make test         # Run tests
make test-cov     # Run tests with coverage
make lint         # Check code style
make format       # Auto-format code
make type-check   # Run type checker
make security     # Run security checks
make docs         # Build documentation
make serve-docs   # Serve docs locally
```

## Code Style

- Follow existing patterns in codebase
- Use type hints for all public functions
- Docstrings: Google style
- Line length: 88 (Ruff/Black default)
- Imports: sorted by Ruff (isort rules)

## Classifiers

When setting up or updating `pyproject.toml`:
1. Choose appropriate Development Status (Alpha/Beta/Production)
2. Uncomment relevant Intended Audience entries
3. Add Environment classifier if CLI tool (`Environment :: Console`)
4. Add `Typing :: Typed` if package has type hints
5. Select relevant Topic classifiers for discoverability

See `CLASSIFIERS_REFERENCE.md` in templates for full options.

## Testing Requirements

- All new features require tests
- Maintain >80% coverage
- Run `make test-cov` before PR

## Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

| Type | Description |
|------|-------------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation changes |
| `refactor:` | Code refactoring |
| `test:` | Adding/updating tests |
| `chore:` | Maintenance tasks |
| `perf:` | Performance improvements |

**Important**: Never add `Co-authored-by` lines to commit messages.

## Security

- Never commit secrets/keys
- Run `make security` before PR
- Check bandit findings for issues

## Project Structure

```
count_tokens/
├── src/count_tokens/    # Source code
├── tests/               # Test files
├── docs/                # Documentation
├── pyproject.toml       # Project configuration
├── Makefile             # Development commands
└── README.md            # Project readme
```

## Release Process

```bash
make release-patch  # 0.1.0 → 0.1.1
make release-minor  # 0.1.0 → 0.2.0
make release-major  # 0.1.0 → 1.0.0
```

## Changes in python version in pyproject.toml

When changing the python version in `pyproject.toml`, ensure to also update:
- the python version in the GitHub workflows located in `.github/workflows/`.
- target python version in ruff.toml located in the project root.

## Documentation

When creating or updating documentation, ensure to:
- keep the documentation in the `docs/` folder up to date.
- if applicable, update the `README.md` file in the project root.
- for the mkdocs based documentation, ensure that:
    - it contains my real name: Krystian Safjan
    - links to my personal website: https://safjan.com

## Visibility Helper Generation

When asked to help with project visibility, promotion, or discoverability, generate `.visibility-helper.md` (git-ignored) containing:

1. **GitHub Topics**: 5-10 relevant tags for the repository
2. **Repository Descriptions**: Short (under 100 chars), medium, and detailed variants
3. **Social Preview Image Prompts**: DALL-E/Midjourney prompts for generating social preview image (1280x640)
4. **VHS Tape Script**: Script for [VHS](https://github.com/charmbracelet/vhs) to create terminal demo GIF
5. **Social Media Posts**: Templates for Twitter/X, LinkedIn, Reddit r/Python
6. **Blog Post Outline**: Structure for announcement blog post
7. **PyPI Keywords**: Suggested keywords for pyproject.toml

Reference `VISIBILITY_CHECKLIST.md` for the complete promotion checklist.
