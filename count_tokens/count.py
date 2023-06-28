#!/usr/bin/env python3
import argparse

import pathlib
import tiktoken


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Return the number of tokens in a text string.

    Args:
        string: The text string to count the tokens in.
        encoding_name: The name of the encoding to use.

    Returns:
        The number of tokens in the text string.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))


def count_tokens(file_path: str, encoding_name: str):
    """Return the number of tokens in a text file.

    Args:
        file_path: The path to the text file to count the tokens in.
        encoding_name: The name of the encoding to use.

    Returns:
        The number of tokens in the text file.
    """
    text = pathlib.Path(file_path).read_text()
    return num_tokens_from_string(text, encoding_name)


def main():
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

    args = parser.parse_args()
    file_path = args.file
    encoding_name = args.encoding

    num_tokens = count_tokens(file_path, encoding_name)
    if not args.quiet:
        print(f"File: {file_path}")
        print(f"Encoding: {encoding_name}")
        print(f"Number of tokens: {num_tokens}")
    else:
        print(num_tokens)


if __name__ == "__main__":
    main()
