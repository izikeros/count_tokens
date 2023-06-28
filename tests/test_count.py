import subprocess

import pytest


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
