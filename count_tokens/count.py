#!/usr/bin/env python3
import argparse
import pathlib

import tiktoken

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
    file_path: str, encoding_name: str = "cl100k_base", approximate: str = None
) -> int:
    """Return the number of tokens in a text file.

    Args:
        file_path: The path to the text file to count the tokens in.
        encoding_name: The name of the encoding to use. Default: cl100k_base
        approximate: Approximate the number of tokens without tokenizing. Base on: w - words, c - characters

    Returns:
        The number of tokens in the text file.
    """
    text = pathlib.Path(file_path).read_text()
    if approximate is None:
        return count_tokens_in_string(text, encoding_name)
    elif approximate == "w":
        return int(len(text.split()) * TOKENS_PER_WORD)
    elif approximate == "c":
        return int(len(text) / CHARACTERS_PER_TOKEN)
    return count_tokens_in_string(text, encoding_name)


def main():
    """Run the command line interface.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Count the number of tokens in a text file."
    )
    parser.add_argument("file", help="Path to the input text file")

    # add option -q quiets the output
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Print only the number of tokens"
    )

    # add option -e to specify the encoding
    parser.add_argument(
        "-e",
        "--encoding",
        default="cl100k_base",
        help="Encoding to use (default: cl100k_base)",
    )
    # add option -a approximates the number of tokens
    parser.add_argument(
        "-a",
        "--approx",
        default=None,
        help="Approximate the number of tokens without tokenizing. Base on: w - words, c - characters",
    )

    args = parser.parse_args()
    file_path = args.file
    encoding_name = args.encoding
    approximate = args.approx

    num_tokens = count_tokens_in_file(
        file_path=file_path, encoding_name=encoding_name, approximate=approximate
    )
    if not args.quiet:
        print(f"File: {file_path}")
        print(f"Encoding: {encoding_name}")
        print(f"Number of tokens: {num_tokens}")
    else:
        print(num_tokens)


if __name__ == "__main__":
    main()
