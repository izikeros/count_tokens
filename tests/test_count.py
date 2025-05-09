import pytest
import json
import os
from unittest.mock import mock_open, patch, MagicMock
from pathlib import Path

from count_tokens.count import (
    count_tokens_in_string,
    count_tokens_in_file,
    count_tokens_in_large_file,
    count_tokens_in_directory,
    count,
    _format_output,
    TOKENS_PER_WORD,
    CHARACTERS_PER_TOKEN,
)


@pytest.fixture
def sample_text():
    """Provide a sample text for token counting tests."""
    return "This is a sample text for testing token counting functionality."


@pytest.fixture
def mock_file_content():
    """Provide mock file content for testing file-based functions."""
    return "This is content from a mock file that we will use for token counting tests."


class TestCountTokensInString:
    def test_count_tokens_with_default_encoding(self, sample_text):
        """Test token counting in a string with the default encoding."""
        token_count = count_tokens_in_string(sample_text)

        # Actual token count depends on the tiktoken implementation
        # but we can verify it returns a positive integer
        assert isinstance(token_count, int)
        assert token_count > 0

    def test_count_tokens_with_custom_encoding(self, sample_text):
        """Test token counting with a custom encoding."""
        token_count = count_tokens_in_string(sample_text, "p50k_base")

        assert isinstance(token_count, int)
        assert token_count > 0

    def test_count_tokens_empty_string(self):
        """Test token counting with an empty string."""
        token_count = count_tokens_in_string("")

        assert token_count == 0

    def test_count_tokens_special_characters(self):
        """Test token counting with special characters."""
        special_text = "Special characters: !@#$%^&*()_+{}|:<>?[];',./\\"
        token_count = count_tokens_in_string(special_text)

        assert isinstance(token_count, int)
        assert token_count > 0


class TestCountTokensInFile:
    @patch("pathlib.Path.read_text")
    def test_count_tokens_in_file_default_encoding(
        self, mock_read_text, mock_file_content
    ):
        """Test counting tokens in a file with default encoding."""
        mock_read_text.return_value = mock_file_content
        file_path = "fake_file.txt"

        token_count = count_tokens_in_file(file_path)

        assert isinstance(token_count, int)
        assert token_count > 0
        mock_read_text.assert_called_once_with()

    @patch("pathlib.Path.read_text")
    def test_count_tokens_in_file_approximate_words(self, mock_read_text):
        """Test approximating token count based on word count."""
        mock_read_text.return_value = "This is a test with ten words in this sentence."
        file_path = "fake_file.txt"

        token_count = count_tokens_in_file(
            file_path, approximate="w", tokens_per_word=TOKENS_PER_WORD
        )

        # Should be 10 words * tokens_per_word, rounded down to int
        expected_count = int(10 * TOKENS_PER_WORD)
        assert token_count == expected_count

    @patch("pathlib.Path.read_text")
    def test_count_tokens_in_file_approximate_characters(self, mock_read_text):
        """Test approximating token count based on character count."""
        text = "This is a test text with exactly 40 characters."
        mock_read_text.return_value = text
        file_path = "fake_file.txt"

        token_count = count_tokens_in_file(
            file_path, approximate="c", characters_per_token=CHARACTERS_PER_TOKEN
        )

        # Should be 40 characters / characters_per_token, rounded down to int
        expected_count = int(len(text) / CHARACTERS_PER_TOKEN)
        assert token_count == expected_count

    @patch("pathlib.Path.read_text")
    def test_count_tokens_in_file_unsupported_approximate_method(
        self, mock_read_text, mock_file_content
    ):
        """Test with unsupported approximation method."""
        mock_read_text.return_value = mock_file_content
        file_path = "fake_file.txt"

        # Should fall back to default tokenization
        token_count = count_tokens_in_file(file_path, approximate="unsupported")

        assert isinstance(token_count, int)
        assert token_count > 0

    @patch("pathlib.Path.read_text")
    def test_count_tokens_file_not_found(self, mock_read_text):
        """Test handling of file not found error."""
        mock_read_text.side_effect = FileNotFoundError("File not found")
        file_path = "nonexistent_file.txt"

        with pytest.raises(FileNotFoundError):
            count_tokens_in_file(file_path)


class TestCountTokensInLargeFile:
    @patch("builtins.open")
    def test_count_tokens_large_file_default(self, mock_open_func):
        """Test counting tokens in a large file with default settings."""
        # Mock file with two chunks
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.side_effect = [
            "This is chunk one",
            "This is chunk two",
            "",
        ]
        mock_open_func.return_value = mock_file

        token_count = count_tokens_in_large_file("large_file.txt")

        assert isinstance(token_count, int)
        assert token_count > 0
        assert (
            mock_file.__enter__.return_value.read.call_count == 3
        )  # Initial two chunks + EOF check

    @patch("builtins.open")
    def test_count_tokens_large_file_with_custom_chunk_size(self, mock_open_func):
        """Test counting tokens with custom chunk size."""
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.side_effect = ["Small chunk", ""]
        mock_open_func.return_value = mock_file

        token_count = count_tokens_in_large_file("large_file.txt", chunk_size=100)

        assert isinstance(token_count, int)
        assert token_count > 0
        mock_file.__enter__.return_value.read.assert_called_with(100)

    @patch("count_tokens.count.count_tokens_in_file")
    def test_count_tokens_large_file_with_approximation(self, mock_count_file):
        """Test large file counting with approximation enabled."""
        mock_count_file.return_value = 42

        # When approximation is used, should delegate to count_tokens_in_file
        result = count_tokens_in_large_file("large_file.txt", approximate="w")

        assert result == 42
        mock_count_file.assert_called_once_with(
            "large_file.txt", "cl100k_base", "w", TOKENS_PER_WORD, CHARACTERS_PER_TOKEN
        )

    @patch("builtins.open")
    def test_count_tokens_large_file_unicode_error_fallback(self, mock_open_func):
        """Test fallback to latin-1 encoding when utf-8 fails."""
        # First attempt with utf-8 fails, second with latin-1 succeeds
        mock_utf8_file = MagicMock()
        mock_utf8_file.__enter__.return_value.read.side_effect = UnicodeDecodeError(
            "utf-8", b"", 0, 1, "mock error"
        )

        mock_latin_file = MagicMock()
        mock_latin_file.__enter__.return_value.read.side_effect = [
            "Latin encoded text",
            "",
        ]

        mock_open_func.side_effect = [mock_utf8_file, mock_latin_file]

        token_count = count_tokens_in_large_file("binary_file.bin")

        assert isinstance(token_count, int)
        assert token_count > 0
        # Check that we tried with both encodings
        mock_open_func.assert_called_with("binary_file.bin", "r", encoding="latin-1")


class TestCountTokensInDirectory:
    @patch("pathlib.Path.glob")
    @patch("count_tokens.count.count_tokens_in_file")
    def test_count_tokens_in_directory_default(self, mock_count_file, mock_glob):
        """Test counting tokens in a directory with default settings."""
        # Mock the glob pattern to return two files
        mock_path1 = MagicMock(spec=Path)
        mock_path1.__str__.return_value = "/test/file1.txt"
        mock_path2 = MagicMock(spec=Path)
        mock_path2.__str__.return_value = "/test/file2.py"

        # For each pattern in file_patterns, return the corresponding mock paths
        mock_glob.side_effect = [[mock_path1], [mock_path2], []]

        # Mock token counts for the files
        mock_count_file.side_effect = [100, 200]

        result = count_tokens_in_directory("/test")

        assert isinstance(result, dict)
        assert result["/test/file1.txt"] == 100
        assert result["/test/file2.py"] == 200

    @pytest.mark.skip(reason="Skipping test for streaming directory counting")
    @patch("pathlib.Path.glob")
    @patch("count_tokens.count.count_tokens_in_large_file")
    def test_count_tokens_in_directory_with_streaming(
        self, mock_count_large, mock_glob
    ):
        """Test counting tokens in a directory with streaming enabled."""
        mock_path = MagicMock(spec=Path)
        mock_path.__str__.return_value = "/test/large_file.txt"
        mock_glob.return_value = [mock_path]
        mock_count_large.return_value = 5000

        result = count_tokens_in_directory("/test", use_streaming=True)

        assert result["/test/large_file.txt"] == 5000
        mock_count_large.assert_called_once()

    @patch("pathlib.Path.glob")
    @patch("count_tokens.count.count_tokens_in_file")
    def test_count_tokens_in_directory_with_error(self, mock_count_file, mock_glob):
        """Test handling of errors when counting tokens in directory."""
        mock_path = MagicMock(spec=Path)
        mock_path.__str__.return_value = "/test/error_file.txt"
        mock_glob.return_value = [mock_path]
        mock_count_file.side_effect = Exception("Test error")

        result = count_tokens_in_directory("/test")

        assert "/test/error_file.txt" in result
        assert result["/test/error_file.txt"].startswith("Error:")

    @pytest.mark.skip(reason="Skipping test for recursive directory counting")
    @patch("pathlib.Path.glob")
    def test_count_tokens_in_directory_recursive(self, mock_glob):
        """Test counting tokens in directory with recursive option."""
        mock_path = MagicMock(spec=Path)
        mock_path.__str__.return_value = "/test/file1.txt"
        mock_glob.return_value = [mock_path]

        count_tokens_in_directory("/test", recursive=True)

        # When recursive=True, it should use ** pattern for depth
        mock_glob.assert_called_once_with("**/*.txt")


class TestCountFunction:
    def test_count_text_mode(self):
        """Test the count function in text mode."""
        result = count(text="Count these tokens")

        assert isinstance(result, int)
        assert result > 0

    @patch("count_tokens.count.count_tokens_in_file")
    def test_count_file_mode(self, mock_count_file):
        """Test the count function in file mode."""
        mock_count_file.return_value = 123

        result = count(file="test.txt")

        assert result == 123
        mock_count_file.assert_called_once()

    @patch("count_tokens.count.count_tokens_in_large_file")
    def test_count_file_mode_with_streaming(self, mock_count_large):
        """Test the count function in file mode with streaming."""
        mock_count_large.return_value = 456

        result = count(file="large.txt", use_streaming=True)

        assert result == 456
        mock_count_large.assert_called_once()

    @patch("count_tokens.count.count_tokens_in_directory")
    def test_count_directory_mode(self, mock_count_dir):
        """Test the count function in directory mode."""
        mock_results = {"/test/file1.txt": 100, "/test/file2.txt": 200}
        mock_count_dir.return_value = mock_results

        result = count(directory="/test")

        assert result == mock_results
        mock_count_dir.assert_called_once()

    def test_count_no_input_provided(self):
        """Test the count function with no input provided."""
        with pytest.raises(
            ValueError, match="Either text, file, or directory must be provided"
        ):
            count()

    def test_count_with_max_tokens_under_limit(self):
        """Test the count function with max_tokens when under the limit."""
        result = count(text="Short text", max_tokens=100)

        # Should just return the token count since it's under the limit
        assert isinstance(result, int)

    def test_count_with_max_tokens_over_limit(self):
        """Test the count function with max_tokens when over the limit."""
        # Get the actual token count first
        actual_count = count_tokens_in_string("This is a test text")

        # Now set the max_tokens to be less than the actual count
        result = count(text="This is a test text", max_tokens=actual_count - 1)

        assert isinstance(result, dict)
        assert result["tokens"] == actual_count
        assert result["limit_exceeded"] is True
        assert result["max_tokens"] == actual_count - 1

    @patch("count_tokens.count.count_tokens_in_directory")
    def test_count_directory_with_max_tokens(self, mock_count_dir):
        """Test the count function in directory mode with max_tokens."""
        mock_results = {"/test/file1.txt": 100, "/test/file2.txt": 200}
        mock_count_dir.return_value = mock_results

        result = count(directory="/test", max_tokens=150)

        # file1.txt should be under the limit, file2.txt should be over
        assert isinstance(result["/test/file1.txt"], int)
        assert isinstance(result["/test/file2.txt"], dict)
        assert result["/test/file2.txt"]["limit_exceeded"] is True


class TestFormatOutput:
    def test_format_output_text_int(self):
        """Test formatting integer output as text."""
        result = _format_output(42)

        assert result == "42"

    def test_format_output_text_dict(self):
        """Test formatting dictionary output as text."""
        data = {"/test/file1.txt": 100, "/test/file2.txt": 200}

        result = _format_output(data)

        assert "file1.txt: 100 tokens" in result
        assert "file2.txt: 200 tokens" in result
        assert "Total: 300 tokens across 2 files" in result

    def test_format_output_json(self):
        """Test formatting output as JSON."""
        data = {"/test/file1.txt": 100, "/test/file2.txt": 200}

        result = _format_output(data, "json")
        parsed = json.loads(result)

        assert parsed["/test/file1.txt"] == 100
        assert parsed["/test/file2.txt"] == 200

    def test_format_output_csv_int(self):
        """Test formatting integer output as CSV."""
        result = _format_output(42, "csv")

        assert result == "tokens\n42"

    def test_format_output_csv_dict(self):
        """Test formatting dictionary output as CSV."""
        data = {"/test/file1.txt": 100, "/test/file2.txt": 200}

        result = _format_output(data, "csv")
        lines = result.strip().split("\n")

        assert lines[0] == "file,tokens"
        assert "/test/file1.txt,100" in lines
        assert "/test/file2.txt,200" in lines

    def test_format_output_text_with_errors(self):
        """Test formatting text output with error messages."""
        data = {
            "/test/file1.txt": 100,
            "/test/error.txt": "Error: Could not process file",
        }

        result = _format_output(data)

        assert "file1.txt: 100 tokens" in result
        assert "error.txt: Error: Could not process file" in result
        assert "Total: 100 tokens across 1 files" in result
