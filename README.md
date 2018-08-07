
# Hazy Toolbelt

The Hazy Toolbelt is the command line interface (CLI) to the [Hazy](https://hazy.com) web service. It's developed in Python and the code is published under the [MIT License](https://github.com/hazy/toolbelt/blob/master/LICENSE) at [github.com/hazy/toolbelt](https://github.com/hazy/toolbelt).


## Status - WIP

This toolbelt and the JSON API that it targets are both under active development and are not ready for general use yet.

## Install

### Use

The toolbelt is designed to be used as a pre-built standalone binary. One way to get up and running is to download the latest binary for your architecture from the [releases page](https://github.com/hazy/toolbelt/releases) and put the binary file somewhere on your PATH.

Alternatively on OSX you can install using Homebrew:

```sh
brew tap hazy/toolbelt
brew install hazy
```

Or if you're using Python3, you can install directly from PyPI:

```sh
pip install hazy
```

### Develop

You can install the toolbelt for local development by installing the dependencies into a Python3 environment and developing the egg:

```sh
pip install -r requirements.txt
python setup.py develop
```

This will install a `hazy` binary in your local Python environment's bin folder. You can check that this is on your path with e.g.:

```sh
which hazy
```

### Build

*Note that as of time of writing (7th August 2018) PyInstaller is verified as working with Python 3.6 and has some issues under 3.7.*

You can build a standalone `hazy` binary (for your architecture) using PyInstaller. This requires additional dependencies.

First ensure you have [Pandoc](https://pandoc.org/installing.html), for example using Homebrew:

```sh
brew install pandoc
```

Then install the additional python dependencies:

```sh
pip install -r maintainer-requirements.txt
```

You can then build using:

```sh
./_build.sh
```

This will write a standalone binary to `./dist/hazy`. You can optionally copy this to `/usr/local/bin/hazy` using:

```sh
./_link.sh
```

### Release

You can publish a new version of the toolbelt to PyPI by bumping the version number in `./VERSION` and running:

```sh
./_release.sh
```

TODO:

- [ ] update release script to publish binaries
- [ ] build binaries for multiple platforms


## Usage

Run the `hazy` command without arguments or with the `--help` flag for usage information:

```sh
hazy --help
```

You can drill down into usage information for the resources / command groups and for individual commands, e.g.:

```sh
hazy auth --help
hazy auth login --help
```

Further [documentation is available on the Hazy website](https://hazy.com/docs).


## Test

Running the tests requires `nose` and `coverage`, included in the `maintainer-requirements.txt`.

Then, run e.g.:

```sh
nosetests --with-coverage --cover-package hazy
```
