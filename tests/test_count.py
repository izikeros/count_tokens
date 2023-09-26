import subprocess

import pytest

from count import count_tokens_in_file, count_tokens_in_string


# TODO: KS: 2023-06-28: not implemented yet
@pytest.mark.skip(reason="not implemented yet")
def test_count():
    # Run the script with the -q option
    result = subprocess.run(
        ["python3", "count_tokens/count.py", "tests/doc.txt", "-q"],
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "67"


# programmatic access
def test_count_tokens_in_file():
    assert count_tokens_in_file("doc.txt", "cl100k_base") == 67


def test_count_tokens_in_string():
    assert count_tokens_in_string("This is a test.", "cl100k_base") == 5
