from pathlib import Path

import pytest

# ...existing code...

@pytest.fixture
def docs_dir():
    """Fixture to return the absolute path to the tests/docs directory."""
    return Path(__file__).parent / "docs"
