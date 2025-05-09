#!/usr/bin/env python3
import argparse
import pathlib
import os
import json
import csv
from typing import Dict, List, Union

import tiktoken

# Default values for token estimation
TOKENS_PER_WORD = 4.0 / 3.0
CHARACTERS_PER_TOKEN = 4.0


def count_tokens_in_string(string: str, encoding_name: str = "cl100k_base") -> int:
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
    encoding_name: str = "cl100k_base",
    approximate: str = None,
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


def count_tokens_in_large_file(
    file_path: str, 
    encoding_name: str = "cl100k_base",
    chunk_size: int = 1024*1024,  # 1MB chunks
    approximate: str = None,
    tokens_per_word: float = TOKENS_PER_WORD,
    characters_per_token: float = CHARACTERS_PER_TOKEN,
) -> int:
    """Count tokens in a large file by streaming in chunks.
    
    Args:
        file_path: Path to the file
        encoding_name: Encoding to use
        chunk_size: Size of chunks to read in bytes
        approximate: Approximate the number of tokens without tokenizing. Base on: w - words, c - characters
        tokens_per_word: The number of tokens per word for word-based approximation. Default: 4/3
        characters_per_token: The number of characters per token for character-based approximation. Default: 4
        
    Returns:
        Total token count
    """
    if approximate is not None:
        # For approximation methods, we can just read the whole file and count
        return count_tokens_in_file(
            file_path, encoding_name, approximate, tokens_per_word, characters_per_token
        )
    
    encoding = tiktoken.get_encoding(encoding_name)
    total_tokens = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                total_tokens += len(encoding.encode(chunk))
    except UnicodeDecodeError:
        # Try with a different encoding if utf-8 fails
        with open(file_path, 'r', encoding='latin-1') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                total_tokens += len(encoding.encode(chunk))
            
    return total_tokens


def count_tokens_in_directory(
    directory_path: str,
    file_patterns: List[str] = ["*.txt", "*.py", "*.md"],
    recursive: bool = False,
    encoding_name: str = "cl100k_base",
    use_streaming: bool = False,
    chunk_size: int = 1024*1024,
    approximate: str = None,
    tokens_per_word: float = TOKENS_PER_WORD,
    characters_per_token: float = CHARACTERS_PER_TOKEN,
) -> Dict[str, Union[int, str]]:
    """Count tokens in multiple files matching patterns in a directory.

    Args:
        directory_path: Path to directory to scan
        file_patterns: List of glob patterns to match files
        recursive: Whether to search subdirectories
        encoding_name: The name of the encoding to use
        use_streaming: Whether to use streaming for large files
        chunk_size: Size of chunks to read in bytes (for streaming)
        approximate: Approximate the number of tokens without tokenizing
        tokens_per_word: The number of tokens per word for approximation
        characters_per_token: The number of characters per token for approximation

    Returns:
        Dict mapping filenames to token counts
    """
    results = {}
    base_path = pathlib.Path(directory_path)

    for pattern in file_patterns:
        if recursive:
            glob_pattern = f"**/{pattern}"
        else:
            glob_pattern = pattern

        for file_path in base_path.glob(glob_pattern):
            try:
                if use_streaming:
                    results[str(file_path)] = count_tokens_in_large_file(
                        str(file_path),
                        encoding_name=encoding_name,
                        chunk_size=chunk_size,
                        approximate=approximate,
                        tokens_per_word=tokens_per_word,
                        characters_per_token=characters_per_token,
                    )
                else:
                    results[str(file_path)] = count_tokens_in_file(
                        str(file_path),
                        encoding_name=encoding_name,
                        approximate=approximate,
                        tokens_per_word=tokens_per_word,
                        characters_per_token=characters_per_token,
                    )
            except Exception as e:
                results[str(file_path)] = f"Error: {str(e)}"

    return results


# Simple API for common use cases
def count(
    text: str = None, 
    file: str = None, 
    directory: str = None,
    encoding: str = "cl100k_base",
    file_patterns: List[str] = ["*.txt", "*.py", "*.md"],
    recursive: bool = False,
    use_streaming: bool = False,
    chunk_size: int = 1024*1024,
    approximate: str = None,
    tokens_per_word: float = TOKENS_PER_WORD,
    characters_per_token: float = CHARACTERS_PER_TOKEN,
    max_tokens: int = None,
):
    """Count tokens with a simplified API.
    
    Args:
        text: Text string to count (optional)
        file: File path to count (optional)
        directory: Directory path to count (optional)
        encoding: Encoding to use
        file_patterns: List of glob patterns when using directory mode
        recursive: Whether to search subdirectories
        use_streaming: Whether to use streaming for large files
        chunk_size: Size of chunks to read in bytes (for streaming)
        approximate: Approximate the number of tokens without tokenizing
        tokens_per_word: The number of tokens per word for approximation
        characters_per_token: The number of characters per token for approximation
        max_tokens: Optional maximum token limit to check against
        
    Returns:
        Token count or dictionary of counts for directory mode
    """
    result = None
    
    if text is not None:
        result = count_tokens_in_string(text, encoding)
    elif file is not None:
        if use_streaming:
            result = count_tokens_in_large_file(
                file, 
                encoding_name=encoding,
                chunk_size=chunk_size,
                approximate=approximate,
                tokens_per_word=tokens_per_word,
                characters_per_token=characters_per_token,
            )
        else:
            result = count_tokens_in_file(
                file, 
                encoding_name=encoding,
                approximate=approximate,
                tokens_per_word=tokens_per_word,
                characters_per_token=characters_per_token,
            )
    elif directory is not None:
        result = count_tokens_in_directory(
            directory, 
            file_patterns=file_patterns, 
            recursive=recursive, 
            encoding_name=encoding,
            use_streaming=use_streaming,
            chunk_size=chunk_size,
            approximate=approximate,
            tokens_per_word=tokens_per_word,
            characters_per_token=characters_per_token,
        )
    else:
        raise ValueError("Either text, file, or directory must be provided")
    
    # Check if result exceeds max_tokens if specified
    if max_tokens is not None:
        if isinstance(result, int) and result > max_tokens:
            return {"tokens": result, "limit_exceeded": True, "max_tokens": max_tokens}
        elif isinstance(result, dict):
            # Add limit_exceeded flag to each file that exceeds the limit
            for file_path, count in list(result.items()):
                if isinstance(count, int) and count > max_tokens:
                    result[file_path] = {"tokens": count, "limit_exceeded": True, "max_tokens": max_tokens}
    
    return result


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
            output = []
            output.append("file,tokens")
            for file_path, count in results.items():
                output.append(f"{file_path},{count}")
            return "\n".join(output)
        return f"tokens\n{results}"
    else:  # text format (default)
        if isinstance(results, dict):
            output = []
            total = 0
            for file_path, count in results.items():
                if isinstance(count, int):
                    output.append(f"{file_path}: {count} tokens")
                    total += count
                else:
                    output.append(f"{file_path}: {count}")
            output.append(f"\nTotal: {total} tokens across {len([c for c in results.values() if isinstance(c, int)])} files")
            return "\n".join(output)
        return str(results)


def main():
    """Run the command line interface.

    Returns:
        None
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
        default="cl100k_base",
        help="Encoding to use (default: cl100k_base)",
    )
    parser.add_argument(
        "-a",
        "--approx",
        default=None,
        help="Approximate the number of tokens without tokenizing. Base on: w - words, c - characters",
    )

    # Directory processing options
    parser.add_argument("-d", "--directory", help="Process all matching files in directory")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process directories recursively")
    parser.add_argument("-p", "--pattern", default="*.txt", help="File pattern when using directory mode (comma-separated)")

    # Output format options
    parser.add_argument("--format", choices=["text", "json", "csv"], default="text", help="Output format")
    
    # Large file handling
    parser.add_argument("--stream", action="store_true", help="Use streaming mode for large files")
    parser.add_argument("--chunk-size", type=int, default=1024*1024, help="Chunk size for streaming mode (bytes)")
    
    # Token limit checking
    parser.add_argument("--max-tokens", type=int, help="Check if tokens exceed this limit")

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

    args = parser.parse_args()

    # Common parameters
    encoding_name = args.encoding
    approximate = args.approx
    tokens_per_word = args.tokens_per_word
    characters_per_token = args.characters_per_token
    output_format = args.format
    use_streaming = args.stream
    chunk_size = args.chunk_size

    # Determine operation mode and get results
    results = None

    # Directory mode
    if args.directory:
        patterns = args.pattern.split(",")
        results = count_tokens_in_directory(
            directory_path=args.directory,
            file_patterns=[p.strip() for p in patterns],
            recursive=args.recursive,
            encoding_name=encoding_name,
            use_streaming=use_streaming,
            chunk_size=chunk_size,
            approximate=approximate,
            tokens_per_word=tokens_per_word,
            characters_per_token=characters_per_token,
        )
    # Single file mode
    elif args.file:
        file_path = args.file
        if use_streaming:
            num_tokens = count_tokens_in_large_file(
                file_path=file_path,
                encoding_name=encoding_name,
                chunk_size=chunk_size,
                approximate=approximate,
                tokens_per_word=tokens_per_word,
                characters_per_token=characters_per_token,
            )
        else:
            num_tokens = count_tokens_in_file(
                file_path=file_path,
                encoding_name=encoding_name,
                approximate=approximate,
                tokens_per_word=tokens_per_word,
                characters_per_token=characters_per_token,
            )

        if not args.quiet and output_format == "text":
            print(f"File: {file_path}")
            print(f"Encoding: {encoding_name}")
            if approximate == "w":
                print(f"Approximation method: Words (tokens per word: {tokens_per_word})")
            elif approximate == "c":
                print(
                    f"Approximation method: Characters (characters per token: {characters_per_token})"
                )
            print(f"Number of tokens: {num_tokens}")
            return
        results = num_tokens
    else:
        parser.print_help()
        return

    # Print results according to format
    if args.quiet:
        if isinstance(results, dict):
            total = sum(count for count in results.values() if isinstance(count, int))
            print(total)
        else:
            print(results)
    else:
        print(_format_output(results, output_format))


if __name__ == "__main__":
    main()
