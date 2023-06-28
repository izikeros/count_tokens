# Count tokens

![img](https://img.shields.io/pypi/v/count-tokens.svg)
![](https://img.shields.io/pypi/pyversions/count-tokens.svg)
![](https://img.shields.io/pypi/dm/count-tokens.svg)


Simple tool that have one purpose - count tokens in a text file.

## Requirements

This package is using [tiktoken](https://github.com/openai/tiktoken) library for tokenization.

```shell

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

## Related Projects
- [tiktoken](https://github.com/openai/tiktoken) - tokenization library used by this package

## Credits

Thanks to the authors of the tiktoken library for open sourcing their work.

## License

[MIT](https://izikeros.mit-license.org/) © [Krystian Safjan](https://safjan.com).
