# Getting Started

## Installation

### Using pip

```bash
pip install count-tokens
```

### Using uv

```bash
uv add count-tokens
```

### From source

```bash
git clone https://github.com/izikeros/count_tokens
cd count_tokens
uv sync
```

## CLI Usage

The `count-tokens` CLI provides a simple way to count tokens in files.

### Basic usage

```bash
count-tokens myfile.txt
```

### Available options

```bash
count-tokens --help
```

### Specifying encoding

```bash
count-tokens myfile.txt --encoding cl100k_base
```

Available encodings:
- `cl100k_base` - Used by GPT-4 and GPT-3.5-turbo
- `p50k_base` - Used by Codex models
- `r50k_base` - Used by GPT-3 models

## Python API Usage

### Count tokens in a file

```python
from count_tokens import count_tokens_in_file

num_tokens = count_tokens_in_file("myfile.txt")
print(f"File contains {num_tokens} tokens")
```

### Count tokens in a string

```python
from count_tokens import count_tokens_in_string

text = "Hello, world! This is a test."
num_tokens = count_tokens_in_string(text)
print(f"String contains {num_tokens} tokens")
```

### Using the main count function

```python
from count_tokens import count

# Returns token count with additional metadata
result = count("myfile.txt")
```
