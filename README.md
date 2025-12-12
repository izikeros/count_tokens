# Count tokens

![img](https://img.shields.io/pypi/v/count-tokens.svg)
![](https://img.shields.io/pypi/pyversions/count-tokens.svg)
![](https://img.shields.io/pypi/dm/count-tokens.svg)
<a href="https://codeclimate.com/github/izikeros/count_tokens/maintainability"><img src="https://api.codeclimate.com/v1/badges/37fd0435fff274b6c9b5/maintainability" /></a>
[![codecov](https://codecov.io/gh/izikeros/count_tokens/branch/main/graph/badge.svg)](https://codecov.io/gh/izikeros/count_tokens)

A versatile tool for counting tokens in text files, directories, and strings with support for streaming large files, batching, and more.

## Table of Contents

- [Count tokens](#count-tokens)
	- [Table of Contents](#table-of-contents)
	- [Requirements](#requirements)
	- [Installation](#installation)
	- [Usage](#usage)
		- [Basic Usage](#basic-usage)
		- [Directory Processing](#directory-processing)
		- [Large File Support](#large-file-support)
		- [Output Formats](#output-formats)
		- [Token Limit Checking](#token-limit-checking)
	- [Approximate number of tokens](#approximate-number-of-tokens)
	- [Adjusting estimation rules](#adjusting-estimation-rules)
	- [Programmatic usage](#programmatic-usage)
		- [Simple API](#simple-api)
		- [Directory Processing](#directory-processing-1)
		- [Streaming Large Files](#streaming-large-files)
		- [Check Token Limits](#check-token-limits)
		- [Original API](#original-api)
	- [Related Projects](#related-projects)
	- [Credits](#credits)
	- [License](#license)

## Requirements

This package is using [tiktoken](https://github.com/openai/tiktoken) library for tokenization.

## Installation

For usage from command line install the package in isolated environment with pipx:

```sh
pipx install count-tokens
```

or run it with [uv](https://github.com/astral-sh/uv) without installing:

```sh
uvx count-tokens document.txt
```

or install it in your current environment with pip.

```sh
pip install count-tokens
```

## Usage

### Basic Usage

Open terminal and run:

```sh
count-tokens document.txt
```

You should see something like this:

```sh
File: document.txt
Encoding: cl100k_base
Number of tokens: 67
```

if you want to see just the tokens count run:

```sh
count-tokens document.txt --quiet
```

and the output will be:

```sh
67
```

To use `count-tokens` with other than default `cl100k_base` encoding use the additional input argument `-e` or `--encoding`:

```sh
count-tokens document.txt -e r50k_base
```

NOTE: `tiktoken` supports three encodings used by OpenAI models:

| Encoding name           | OpenAI models                                       |
|-------------------------|-----------------------------------------------------|
| `o200k_base`            | `gpt-4o`, `gpt-4o-mini`                             |
| `cl100k_base`           | `gpt-4`, `gpt-3.5-turbo`, `text-embedding-ada-002`  |
| `p50k_base`             | Codex models, `text-davinci-002`, `text-davinci-003` |
| `r50k_base` (or `gpt2`) | GPT-3 models like `davinci`                         |

(source: [OpenAI Cookbook](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken))

### Directory Processing

Process all files in a directory matching specific patterns:

```sh
count-tokens -d ./docs -p "*.md,*.txt"
```

If `-p` is not specified, the default patterns are `*.txt,*.py,*.md`.

Process directories recursively:

```sh
count-tokens -d ./project -r -p "*.py"
```

### Large File Support

Use streaming mode for large files to avoid memory issues:

```sh
count-tokens large_file.txt --stream
```

Customize chunk size for streaming (default is 1MB):

```sh
count-tokens large_file.txt --stream --chunk-size 2097152
```

### Output Formats

Get results in different formats:

```sh
# JSON format
count-tokens -d ./docs -p "*.md" --format json

# CSV format
count-tokens -d ./docs -p "*.md" --format csv
```

### Token Limit Checking

Check if files exceed a specific token limit:

```sh
count-tokens document.txt --max-tokens 4096
```

When files exceed the limit, you'll see a warning:

```
File: document.txt
Encoding: cl100k_base
⚠️ Token limit exceeded: 5120 > 4096
Number of tokens: 5120
```

## Approximate number of tokens

In case you need the results a bit faster and you don't need the exact number of tokens you can use the `--approx` parameter with `w` to have approximation based on number of words or `c` to have approximation based on number of characters.

```shell
count-tokens document.txt --approx w
```

It is based on assumption that there is 4/3 (1 and 1/3) tokens per word and 4 characters per token.

## Adjusting estimation rules

You can customize the rules used for token estimation by adjusting the default values for tokens per word and characters per token ratios:

```shell
# Adjust the tokens per word ratio (default is 1.33)
count-tokens document.txt --approx w --tokens-per-word 1.5

# Adjust the characters per token ratio (default is 4.0)
count-tokens document.txt --approx c --characters-per-token 3.5
```

These options allow you to fine-tune the approximation based on your specific content characteristics.

## Programmatic usage

### Simple API

The package now provides a simplified API for all token counting operations:

```python
from count_tokens import count

# Count tokens in a string
result = count(text="This is a string")

# Count tokens in a file
result = count(file="document.txt", encoding="cl100k_base")

# Count tokens with approximation
result = count(file="document.txt", approximate="w", tokens_per_word=1.5)
```

### Directory Processing

Process all files in a directory that match specific patterns:

```python
from count_tokens import count

# Process a directory
results = count(
    directory="./docs",
    file_patterns=["*.md", "*.txt"],
    recursive=True
)

# Print results
for file_path, token_count in results.items():
    print(f"{file_path}: {token_count} tokens")
```

### Streaming Large Files

Process large files without loading the entire file into memory:

```python
from count_tokens import count

# Process a large file with streaming
tokens = count(
    file="large_dataset.txt", 
    use_streaming=True,
    chunk_size=1024*1024  # 1MB chunks
)
```

### Check Token Limits

Check if content exceeds token limits:

```python
from count_tokens import count

# Check if a file exceeds token limit
result = count(file="document.txt", max_tokens=4096)

if isinstance(result, dict) and result.get("limit_exceeded"):
    print(f"⚠️ Token limit exceeded: {result['tokens']} > {result['max_tokens']}")
```

### Original API

The original functions are still available for backward compatibility:

```python
from count_tokens.count import count_tokens_in_file, count_tokens_in_string

# Count tokens in a file
num_tokens = count_tokens_in_file("document.txt")

# Count tokens in a string
num_tokens = count_tokens_in_string("This is a string.")

# Use specific encoding
num_tokens = count_tokens_in_string("This is a string.", encoding_name="cl100k_base")

# Word-based approximation with custom tokens per word ratio
num_tokens = count_tokens_in_file("document.txt", approximate="w", tokens_per_word=1.5)

# Character-based approximation with custom characters per token ratio
num_tokens = count_tokens_in_file("document.txt", approximate="c", characters_per_token=3.5)
```

## Related Projects

- [tiktoken](https://github.com/openai/tiktoken) - tokenization library used by this package
- [ttok](https://github.com/simonw/ttok) - count and truncate text based on tokens

## Credits

Thanks to the authors of the [tiktoken](https://github.com/openai/tiktoken) library for open sourcing their work.

## License

[MIT](https://izikeros.mit-license.org/) © [Krystian Safjan](https://safjan.com).
