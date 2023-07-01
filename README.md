# Count tokens

![img](https://img.shields.io/pypi/v/count-tokens.svg)
![](https://img.shields.io/pypi/pyversions/count-tokens.svg)
![](https://img.shields.io/pypi/dm/count-tokens.svg)
<a href="https://codeclimate.com/github/izikeros/count_tokens/maintainability"><img src="https://api.codeclimate.com/v1/badges/37fd0435fff274b6c9b5/maintainability" /></a>

Simple tool that have one purpose - count tokens in a text file.

## Requirements

This package is using [tiktoken](https://github.com/openai/tiktoken) library for tokenization.


## Installation
For usage from comman line install the package in isolated environement with pipx:

```sh
$ pipx install count-tokens
```

or install it in your current environment with pip.


## Usage
Open terminal and run:

```shell
$ count-tokens document.txt
```

You should see something like this:

```shell
File: document.txt
Encoding: cl100k_base
Number of tokens: 67
```

if you want to see just the tokens count run:

```shell
$ count-tokens document.txt --quiet
```
and the output will be:

```shell
67
```

NOTE: `tiktoken` supports three encodings used by OpenAI models:

| Encoding name           | OpenAI models                                        |
|-------------------------|------------------------------------------------------|
| `cl100k_base`           | `gpt-4`, `gpt-3.5-turbo`, `text-embedding-ada-002`   |
| `p50k_base`             | Codex models, `text-davinci-002`, `text-davinci-003` |
| `r50k_base` (or `gpt2`) | GPT-3 models like `davinci`                          |

to use token-count with other than default `cl100k_base` encoding use the additional input argument `-e` or `--encoding`:

```shell
$ count-tokens document.txt -e r50k_base
```

## Related Projects
- [tiktoken](https://github.com/openai/tiktoken) - tokenization library used by this package

## Credits

Thanks to the authors of the tiktoken library for open sourcing their work.

## License

[MIT](https://izikeros.mit-license.org/) © [Krystian Safjan](https://safjan.com).
