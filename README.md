
# Anon AI Toolbelt

The Anon AI Toolbelt is a command line interface (CLI) tool for managing and anonymising data with the [Anon AI web service](https://anon.ai). It's developed in Python and the code is published under the [MIT License](https://github.com/anon-ai/toolbelt/blob/master/LICENSE) at [github.com/anon-ai/toolbelt](https://github.com/anon-ai/toolbelt).

*Caution: the toolbelt is under active development. Core functionality works but commands and options are liable to change and some of the features that are documented don't yet exist.*

## Installation

Install using `pip` into a Python3 environment:

```bash
pip install anon-ai-toolbelt
```

Note that the toolbelt only works with Python3 and installs dependencies including the [Python Cryptography Toolkit](https://pypi.python.org/pypi/pycrypto).

## Usage

The primary workflow is for a data controller to `push` data into the system and then for data processors to `pull` the data down in anonymised form.

- [anon login](#login)
- [anon push INPUT_FILE RESOURCE](#push)
- [anon pull RESOURCE OUTPUT_FILE](#pull)
- [anon pipe URL OUTPUT_FILE](#pipe)

<!--

- [anon locate RESOURCE](#locate)
- [anon analyse RESOURCE](#analyse)
- [anon inspect RESOURCE](#inspect)
-->

### Login

Login with your API credentials (writes to `~/.config/anon.ai/config.json`):

```bash
anon login
> key: ...
> secret: ...
```

### Push

Push a data snapshot up to ingest and store it.

```bash
anon push foo.dump mydb
```

When ingesting structured data you should specify the data format:

```bash
anon push foo.dump mydb --format postgres
```

In this example, `mydb` is an arbitrary resource name that you use to identify this ingested data source. Subsequent pushes to the same name are usually used to store a new snapshot of the same file or database.

The stored data is encrypted using AES-256 with a per-account encryption key that lives in (and never leaves) a [secure vault](https://www.vaultproject.io/). You can also optionally provide your own encryption key:

```bash
anon push foo.dump mydb --encryption-key LONG_RANDOM_STRING
```

Note that:

1. your encryption key is **never persisted** in our system -- so you have to manage it and give it to any users that you want to share anonymised data with
3. there's no strict requirement on length or format for your encryption key value (we SHA-256 hash it along with your per-account encryption key) but we recommend at least 16 bytes entropy

### Pull

Pull down an anonymised copy of an ingested data snapshot:

```bash
anon pull mydb foo.dump
```

Optionally provide an encryption key (to decrypt the stored data with) and / or configure how you'd like it anonymised:

```bash
anon pull mydb foo.dump --config config.json --encryption-key ...
```

### Pipe

Pipe data through to anonymise it:

```bash
anon pipe http://humanstxt.org/humans.txt /tmp/humans.anon.txt
```

This parses, analyses and anonymises the data on the fly, i.e.: without persisting it. The data source must currently be a URL.

<!--

### Locate

As an alternative to pulling down the data locally, you can get a temporary download URL:

```bash
anon locate mydb
```

This writes a temporary url to stdout. As with `pull`, you can optionally specify an encryption key and configure anonymisation:

```bash
anon locate mydb --config config.json --encryption-key ...
```

You can also control the timeout duration for the URL. This defaults to 30 minutes and can be a maximum of 24 hours:

```bash
anon locate mydb --timeout 2h
```

### Analyse

Analyse a snapshot to get our structural analysis of the data:

```bash
anon analyse mydb > analysis.json
```

### Inspect

Inspect a resource name to list the versions and see its status:

```bash
anon inspect mydb
```

-->

### Versions

You can `pull` specific snapshot versions by targeting them by name:

```bash
anon pull mydb --snapshot someid
```

You can also `push` snapshots up with a specific name:

```bash
anon push foo.sql mydb --snapshot someid
```

### Tab completion

Enable `bash` completion by adding the following to your `.bashrc`:

```bash
eval "$(_ANON_COMPLETE=source anon)"
```

If you use `zsh`, you can emulate bash completion by first adding `bashcompinit` to your `.zshrc`:

```bash
autoload bashcompinit
bashcompinit
eval "$(_ANON_COMPLETE=source anon)"
```

For more information see [https://anon.ai](https://anon.ai)
