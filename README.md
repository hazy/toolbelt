
# Hazy Toolbelt

The Hazy Toolbelt is a command line interface (CLI) tool for managing and anonymising data with [Hazy](https://hazy.com).

It's developed in Python and the code is published under the [MIT License](https://github.com/hazy/toolbelt/blob/master/LICENSE) at [github.com/hazy/toolbelt](https://github.com/hazy/toolbelt).

## Status - WIP

This version of the toolbelt is being re-written with a new command structure to work with the second version of the Hazy console.

It's not ready to use yet.

## Dependencies
On macOS, install Pandoc using Homebrew

```sh
brew install pandoc
```

Refer to [Pandoc Documentation](https://pandoc.org/installing.html) on how to install for various other platforms.

## Install

```sh
pip install -r requirements.txt
pip install -r maintainer-requirements.txt
python setup.py develop
```

## Run

```sh
hazy --help
```

## Test

```sh
nosetests --with-coverage --cover-package hazy
```
