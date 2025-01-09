# Count tokens

![img](https://img.shields.io/pypi/v/count-tokens.svg)
![](https://img.shields.io/pypi/pyversions/count-tokens.svg)
![](https://img.shields.io/pypi/dm/count-tokens.svg)
<a href="https://codeclimate.com/github/izikeros/count_tokens/maintainability"><img src="https://api.codeclimate.com/v1/badges/37fd0435fff274b6c9b5/maintainability" /></a>

Simple tool that has one purpose - count tokens in a text file.

## Table of Contents

- [Count tokens](#count-tokens)
	- [Table of Contents](#table-of-contents)
	- [Requirements](#requirements)
	- [Installation](#installation)
	- [Usage](#usage)
	- [Approximate number of tokens](#approximate-number-of-tokens)
	- [Programmatic usage](#programmatic-usage)
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

or install it in your current environment with pip.

```sh
pip install count-tokens
```

## Usage

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

## Approximate number of tokens

In case you need the results a bit faster and you don't need the exact number of tokens you can use the `--approx` parameter with `w` to have approximation based on number of words or `c` to have approximation based on number of characters.

```shell
count-tokens document.txt --approx w
```

It is based on assumption that there is 4/3 (1 and 1/3) tokens per word and 4 characters per token.

## Programmatic usage

```python
from count_tokens.count import count_tokens_in_file

num_tokens = count_tokens_in_file("document.txt")
```

```python
from count_tokens.count import count_tokens_in_string

num_tokens = count_tokens_in_string("This is a string.")
```

for both functions you can use `encoding` parameter to specify the encoding used by the model:

```python
from count_tokens.count import count_tokens_in_string

num_tokens = count_tokens_in_string("This is a string.", encoding="cl100k_base")
```

Default value for `encoding` is `cl100k_base`.

## Related Projects

- [tiktoken](https://github.com/openai/tiktoken) - tokenization library used by this package
- [ttok](https://github.com/simonw/ttok) - count and truncate text based on tokens

## Credits

Thanks to the authors of the [tiktoken](https://github.com/openai/tiktoken) library for open sourcing their work.

## License

[MIT](https://izikeros.mit-license.org/) © [Krystian Safjan](https://safjan.com).
