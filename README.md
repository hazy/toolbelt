
*Caution: this repo is work in progress under active development. It's likely that many features don't yet exist, let alone work.*

# Anon AI Toolbelt

The Anon AI Toolbelt is a command line interface (CLI) tool for managing and anonymising data with the Anon AI web service.

It's developed in Python and the code is open sourced under the
[MIT License](https://github.com/anon-ai/toolbelt/blob/master/LICENSE)
at [github.com/anon-ai/toolbelt](https://github.com/anon-ai/toolbelt).

## Installation

Current installation is via pip:

```bash
pip install anon-ai-toolbelt
```

## Usage

The primary workflow is for a privileged process or developer to `push` data into the system and then for less-privileged processes, developers or collaborators to `pull` the data down in anonymised form.

Data anonymisation can be configured differently for different users or use cases. This configuration is integrated with a role-based permission system that controls which users can access which aspects of which data.

*Note that the anonymisation configuration options and the role-based permission system are currently unspecified.*

- [anon login](#login)
- [anon pipe INPUT OUTPUT](#pipe)
- [anon push INPUT RESOURCE](#push)
- [anon pull RESOURCE OUTPUT](#pull)
- [anon locate RESOURCE](#locate)
- [anon analyse RESOURCE](#analyse)
- [anon inspect RESOURCE](#inspect)

### Login

Login with your API credentials (writes to `~/.config/anon.ai/config.json`):

```bash
anon login
> key: ...
> secret: ...
```

### Pipe

Pipe data through to anonymise it:

```bash
anon pipe foo.sql result.sql
```

This parses, analyses and anonymises the data on the fly, i.e.: without persisting it. The data source can be a local filepath or a URL:

```bash
anon pipe http://example.com/foo.sql result.sql
```

You can specify the data format and configure how you'd like it anonymised:

```bash
anon pipe foo.sql result.sql --format postgres --config config.json
```

*Note that the anonymisation configuration options are currently unspecified.*

### Push

Push a data snapshot up to ingest and store it.

```bash
anon push foo.dump mydb
```

Format and source options are the same as with `pipe` above, e.g.:

```bash
anon push http://example.com/foo.sql mydb --format postgres
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

### Versions

You can `pull`, `download` and `inspect` specific snapshot versions by targeting them by name:

```bash
anon pull mydb --snapshot someid
anon download mydb --snapshot someid
anon inspect mydb --snapshot someid
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

### Todo

- better repr results (include type, etc.)
- consistent -o --output formatting i.e. yaml, json
- -v --verbose for logging
- bash and zsh tab complete
- coloured output
