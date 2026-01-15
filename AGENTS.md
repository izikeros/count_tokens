# AI Agent Instructions

## Project Overview

Count number of tokens in text files using tiktoken tokenizer from OpenAI.

## Development Commands

```bash
poetry install        # Install dependencies
poetry run pytest     # Run tests
poetry run count-tokens <file>  # Run CLI
```

## Code Style

- Follow existing patterns in codebase
- Use type hints for all public functions
- Docstrings: Google style
- Line length: 88 (Ruff/Black default)
- Imports: sorted by Ruff (isort rules)

## Testing Requirements

- All new features require tests
- Run tests before PR

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
- This tool handles user files - be careful with file operations

## Project Structure

```
count_tokens/
├── count_tokens/     # Source code
│   └── count.py      # Main CLI implementation
├── tests/            # Test files
├── pyproject.toml    # Project configuration (Poetry)
└── README.md         # Project readme
```

## Migration Note

This project is pending migration to the unified standard (uv + Hatchling).
Currently uses Poetry as build system.
