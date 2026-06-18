#!/usr/bin/env python3
import argparse
import csv
import io
import json
import pathlib
from _csv import Writer
from argparse import Namespace
from dataclasses import dataclass, fields

import tiktoken

# Default values for token estimation
TOKENS_PER_WORD = 4.0 / 3.0
CHARACTERS_PER_TOKEN = 4.0

# Default configuration values
DEFAULT_ENCODING = "cl100k_base"
TXT_PATTERN = "*.txt"
DEFAULT_FILE_PATTERNS = [TXT_PATTERN, "*.py", "*.md"]
DEFAULT_CHUNK_SIZE = 1024 * 1024  # 1MB chunks


@dataclass
class TokenCountOptions:
    """Options controlling how tokens are counted.

    Bundles the common counting parameters so functions don't need long
    parameter lists. Legacy keyword arguments are still accepted by the
    counting functions and merged into an instance of this class.

    Attributes:
        encoding_name: The name of the tiktoken encoding to use.
        approximate: Approximation mode: "w" (words), "c" (characters), or None.
        tokens_per_word: Tokens per word for word-based approximation.
        characters_per_token: Characters per token for character-based approximation.
        use_streaming: Whether to stream large files in chunks.
        chunk_size: Size of chunks to read in bytes when streaming.
    """

    encoding_name: str = DEFAULT_ENCODING
    approximate: str | None = None
    tokens_per_word: float = TOKENS_PER_WORD
    characters_per_token: float = CHARACTERS_PER_TOKEN
    use_streaming: bool = False
    chunk_size: int = DEFAULT_CHUNK_SIZE


# Map legacy keyword-argument names to TokenCountOptions field names.
_OPTION_ALIASES = {"encoding": "encoding_name"}


def _merge_options(
    options: TokenCountOptions | None, overrides: dict
) -> TokenCountOptions:
    """Return options updated with any legacy keyword overrides.

    Args:
        options: Base options, or None to start from defaults.
        overrides: Legacy keyword arguments to apply on top of the base options.

    Returns:
        A TokenCountOptions instance reflecting the base options and overrides.

    Raises:
        TypeError: If an override is not a recognized option.
    """
    base = options if options is not None else TokenCountOptions()
    if not overrides:
        return base

    values = {f.name: getattr(base, f.name) for f in fields(TokenCountOptions)}
    for key, value in overrides.items():
        name = _OPTION_ALIASES.get(key, key)
        if name not in values:
            raise TypeError(f"Unexpected keyword argument: {key!r}")
        values[name] = value
    return TokenCountOptions(**values)


def count_tokens_in_string(string: str, encoding_name: str = DEFAULT_ENCODING) -> int:
    """Return the number of tokens in a text string.

    Args:
        string: The text string to count the tokens in.
        encoding_name: The name of the encoding to use. Default: cl100k_base

    Returns:
        The number of tokens in the text string.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))


def count_tokens_in_file(
    file_path: str,
    encoding_name: str = DEFAULT_ENCODING,
    approximate: str | None = None,
    tokens_per_word: float = TOKENS_PER_WORD,
    characters_per_token: float = CHARACTERS_PER_TOKEN,
) -> int:
    """Return the number of tokens in a text file.

    Args:
        file_path: The path to the text file to count the tokens in.
        encoding_name: The name of the encoding to use. Default: cl100k_base
        approximate: Approximate the number of tokens without tokenizing. Base on: w - words, c - characters
        tokens_per_word: The number of tokens per word for word-based approximation. Default: 4/3
        characters_per_token: The number of characters per token for character-based approximation. Default: 4

    Returns:
        The number of tokens in the text file.
    """
    text = pathlib.Path(file_path).read_text()
    if approximate is None:
        return count_tokens_in_string(text, encoding_name)
    elif approximate == "w":
        return int(len(text.split()) * tokens_per_word)
    elif approximate == "c":
        return int(len(text) / characters_per_token)
    return count_tokens_in_string(text, encoding_name)


def _read_chunk_to_boundary(file, chunk_size: int) -> str:
    """Read a chunk from file, extending to the next newline to avoid splitting tokens.

    Args:
        file: Open file object
        chunk_size: Approximate size of chunk to read in bytes

    Returns:
        Text chunk ending at a newline boundary (or EOF)
    """
    chunk = file.read(chunk_size)
    if not chunk:
        return ""

    # If we're not at EOF, read until the next newline to avoid splitting tokens
    if not chunk.endswith("\n"):
        remainder = file.readline()
        chunk += remainder

    return chunk


def _stream_file_tokens(file_path: str, encoding, chunk_size: int) -> int:
    """Stream a file in newline-aligned chunks and count its tokens.

    Falls back to latin-1 if the file is not valid UTF-8.

    Args:
        file_path: Path to the file.
        encoding: A tiktoken encoding instance used to encode chunks.
        chunk_size: Size of chunks to read in bytes.

    Returns:
        Total token count for the file.
    """

    def _count(file_encoding: str) -> int:
        total = 0
        with open(file_path, encoding=file_encoding) as file:
            while True:
                chunk = _read_chunk_to_boundary(file, chunk_size)
                if not chunk:
                    break
                total += len(encoding.encode(chunk))
        return total

    try:
        return _count("utf-8")
    except UnicodeDecodeError:
        return _count("latin-1")


def count_tokens_in_large_file(
    file_path: str,
    options: TokenCountOptions | None = None,
    **kwargs,
) -> int:
    """Count tokens in a large file by streaming in chunks.

    Reads chunks aligned to newline boundaries to avoid splitting tokens
    at arbitrary positions, which would cause inaccurate token counts.

    Args:
        file_path: Path to the file.
        options: Counting options. When None, defaults are used.
        **kwargs: Legacy keyword arguments (encoding_name, chunk_size, approximate,
            tokens_per_word, characters_per_token, use_streaming) merged into options.

    Returns:
        Total token count.
    """
    opts = _merge_options(options, kwargs)

    if opts.approximate is not None:
        # For approximation methods, we can just read the whole file and count
        return count_tokens_in_file(
            file_path,
            opts.encoding_name,
            opts.approximate,
            opts.tokens_per_word,
            opts.characters_per_token,
        )

    encoding = tiktoken.get_encoding(opts.encoding_name)
    return _stream_file_tokens(file_path, encoding, opts.chunk_size)


def _count_single_path(file_path: str, options: TokenCountOptions) -> int:
    """Count tokens for one file using the configured options.

    Args:
        file_path: Path to the file.
        options: Counting options.

    Returns:
        Token count for the file.
    """
    if options.use_streaming:
        return count_tokens_in_large_file(file_path, options)
    return count_tokens_in_file(
        file_path,
        options.encoding_name,
        options.approximate,
        options.tokens_per_word,
        options.characters_per_token,
    )


def count_tokens_in_directory(
    directory_path: str,
    file_patterns: list[str] | None = None,
    recursive: bool = False,
    options: TokenCountOptions | None = None,
    **kwargs,
) -> dict[str, int | str]:
    """Count tokens in multiple files matching patterns in a directory.

    Args:
        directory_path: Path to directory to scan.
        file_patterns: List of glob patterns to match files (default: DEFAULT_FILE_PATTERNS).
        recursive: Whether to search subdirectories.
        options: Counting options. When None, defaults are used.
        **kwargs: Legacy keyword arguments (encoding_name, use_streaming, chunk_size,
            approximate, tokens_per_word, characters_per_token) merged into options.

    Returns:
        Dict mapping filenames to token counts.
    """
    opts = _merge_options(options, kwargs)
    if file_patterns is None:
        file_patterns = list(DEFAULT_FILE_PATTERNS)
    results: dict[str, int | str] = {}
    base_path = pathlib.Path(directory_path)

    for pattern in file_patterns:
        glob_pattern: str = f"**/{pattern}" if recursive else pattern

        for file_path in base_path.glob(glob_pattern):
            try:
                results[str(file_path)] = _count_single_path(str(file_path), opts)
            except Exception as e:
                results[str(file_path)] = f"Error: {e!s}"

    return results


def _apply_max_tokens(result, max_tokens: int | None):
    """Annotate counting results that exceed an optional token limit.

    Args:
        result: An integer token count or a dict of per-file counts.
        max_tokens: Optional maximum token limit to check against.

    Returns:
        The original result, or a dict flagging where the limit is exceeded.
    """
    if max_tokens is None:
        return result

    if isinstance(result, int) and result > max_tokens:
        return {"tokens": result, "limit_exceeded": True, "max_tokens": max_tokens}

    if isinstance(result, dict):
        for file_path, value in list(result.items()):
            if isinstance(value, int) and value > max_tokens:
                result[file_path] = {
                    "tokens": value,
                    "limit_exceeded": True,
                    "max_tokens": max_tokens,
                }

    return result


# Simple API for common use cases
def count(
    text: str | None = None,
    file: str | None = None,
    directory: str | None = None,
    options: TokenCountOptions | None = None,
    max_tokens: int | None = None,
    **kwargs,
):
    """Count tokens with a simplified API.

    Args:
        text: Text string to count (optional).
        file: File path to count (optional).
        directory: Directory path to count (optional).
        options: Counting options. When None, defaults are used.
        max_tokens: Optional maximum token limit to check against.
        **kwargs: Legacy keyword arguments. Counting options (encoding, approximate,
            tokens_per_word, characters_per_token, use_streaming, chunk_size) are merged
            into options; file_patterns and recursive control directory mode.

    Returns:
        Token count or dictionary of counts for directory mode.
    """
    file_patterns = kwargs.pop("file_patterns", None) or list(DEFAULT_FILE_PATTERNS)
    recursive = kwargs.pop("recursive", False)
    opts = _merge_options(options, kwargs)

    if text is not None:
        result = count_tokens_in_string(text, opts.encoding_name)
    elif file is not None:
        result = _count_single_path(file, opts)
    elif directory is not None:
        result = count_tokens_in_directory(
            directory,
            file_patterns=file_patterns,
            recursive=recursive,
            options=opts,
        )
    else:
        raise ValueError("Either text, file, or directory must be provided")

    return _apply_max_tokens(result, max_tokens)


def _format_output(results, output_format="text"):
    """Format output based on format type.

    Args:
        results: Results to format (int or dict)
        output_format: Format type (text, json, csv)

    Returns:
        Formatted output string
    """
    if output_format == "json":
        return json.dumps(results, indent=2)
    elif output_format == "csv":
        if isinstance(results, dict):
            output = io.StringIO(newline="")
            writer: Writer = csv.writer(output, lineterminator="\n")
            writer.writerow(["file", "tokens"])
            for file_path, count in results.items():
                writer.writerow([file_path, count])
            return output.getvalue().rstrip("\n")
        return f"tokens\n{results}"
    else:  # text format (default)
        if isinstance(results, dict):
            output: list[str] = []
            total = 0
            for file_path, count in results.items():
                if isinstance(count, int):
                    output.append(f"{file_path}: {count} tokens")
                    total += count
                else:
                    output.append(f"{file_path}: {count}")
            output.append(
                f"\nTotal: {total} tokens across {len([c for c in results.values() if isinstance(c, int)])} files"
            )
            return "\n".join(output)
        return str(results)


def _build_parser() -> argparse.ArgumentParser:
    """Build the command line argument parser.

    Returns:
        The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Count the number of tokens in text files."
    )
    parser.add_argument("file", nargs="?", help="Path to the input text file")

    # Basic options
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Print only the number of tokens"
    )
    parser.add_argument(
        "-e",
        "--encoding",
        default=DEFAULT_ENCODING,
        help=f"Encoding to use (default: {DEFAULT_ENCODING})",
    )
    parser.add_argument(
        "-a",
        "--approx",
        default=None,
        help="Approximate the number of tokens without tokenizing. Base on: w - words, c - characters",
    )

    # Directory processing options
    parser.add_argument(
        "-d", "--directory", help="Process all matching files in directory"
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Process directories recursively"
    )
    parser.add_argument(
        "-p",
        "--pattern",
        default=TXT_PATTERN,
        help="File pattern when using directory mode (comma-separated)",
    )

    # Output format options
    parser.add_argument(
        "--format",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format",
    )

    # Large file handling
    parser.add_argument(
        "--stream", action="store_true", help="Use streaming mode for large files"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help="Chunk size for streaming mode (bytes)",
    )

    # Token limit checking
    parser.add_argument(
        "--max-tokens", type=int, help="Check if tokens exceed this limit"
    )

    # Approximation options
    parser.add_argument(
        "--tokens-per-word",
        type=float,
        default=TOKENS_PER_WORD,
        help=f"Number of tokens per word for word-based approximation (default: {TOKENS_PER_WORD})",
    )
    parser.add_argument(
        "--characters-per-token",
        type=float,
        default=CHARACTERS_PER_TOKEN,
        help=f"Number of characters per token for character-based approximation (default: {CHARACTERS_PER_TOKEN})",
    )

    return parser


def _options_from_args(args: Namespace) -> TokenCountOptions:
    """Build TokenCountOptions from parsed CLI arguments.

    Args:
        args: Parsed command line arguments.

    Returns:
        Counting options derived from the arguments.
    """
    return TokenCountOptions(
        encoding_name=args.encoding,
        approximate=args.approx,
        tokens_per_word=args.tokens_per_word,
        characters_per_token=args.characters_per_token,
        use_streaming=args.stream,
        chunk_size=args.chunk_size,
    )


def _print_single_file(
    file_path: str, options: TokenCountOptions, num_tokens: int
) -> None:
    """Print the verbose single-file token report.

    Args:
        file_path: Path of the counted file.
        options: Counting options used.
        num_tokens: The computed token count.
    """
    print(f"File: {file_path}")
    print(f"Encoding: {options.encoding_name}")
    if options.approximate == "w":
        print(
            f"Approximation method: Words (tokens per word: {options.tokens_per_word})"
        )
    elif options.approximate == "c":
        print(
            "Approximation method: Characters "
            f"(characters per token: {options.characters_per_token})"
        )
    print(f"Number of tokens: {num_tokens}")


def _print_results(results, quiet: bool, output_format: str) -> None:
    """Print directory/file results respecting quiet and format settings.

    Args:
        results: An integer token count or a dict of per-file counts.
        quiet: Whether to print only the bare number(s).
        output_format: Output format (text, json, csv).
    """
    if quiet:
        if isinstance(results, dict):
            total = sum(c for c in results.values() if isinstance(c, int))
            print(total)
        else:
            print(results)
    else:
        print(_format_output(results, output_format))


def main() -> None:
    """Run the command line interface.

    Returns:
        None
    """
    parser = _build_parser()
    args: Namespace = parser.parse_args()
    options = _options_from_args(args)

    if args.directory:
        patterns = [p.strip() for p in args.pattern.split(",")]
        results = count_tokens_in_directory(
            args.directory,
            file_patterns=patterns,
            recursive=args.recursive,
            options=options,
        )
    elif args.file:
        num_tokens = _count_single_path(args.file, options)
        if not args.quiet and args.format == "text":
            _print_single_file(args.file, options, num_tokens)
            return
        results = num_tokens
    else:
        parser.print_help()
        return

    _print_results(results, args.quiet, args.format)


if __name__ == "__main__":
    main()
