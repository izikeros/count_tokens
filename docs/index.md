# count-tokens

Count number of tokens in text files using tiktoken tokenizer from OpenAI.

## Features

- Count tokens in files or strings
- Support for multiple OpenAI encodings (cl100k_base, p50k_base, etc.)
- CLI tool for quick token counting
- Python API for integration

## Installation

```bash
pip install count-tokens
```

Or with uv:

```bash
uv add count-tokens
```

## Quick Start

### CLI Usage

```bash
# Count tokens in a file
count-tokens myfile.txt

# Specify encoding
count-tokens myfile.txt --encoding cl100k_base
```

### Python API

```python
from count_tokens import count_tokens_in_file, count_tokens_in_string

# Count tokens in a file
num_tokens = count_tokens_in_file("myfile.txt")

# Count tokens in a string
num_tokens = count_tokens_in_string("Hello, world!")
```

## Links

- [GitHub Repository](https://github.com/izikeros/count_tokens)
- [PyPI Package](https://pypi.org/project/count-tokens/)
