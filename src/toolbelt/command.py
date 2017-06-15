"""Anon AI command line interface.

  Run `anon --help` for usage.
"""

import click
import math
import sys

from . import alias
from . import auth
from . import client

DEFAULT_ENDPOINT="https://api.anon.ai"

@click.command()
@click.option('--key', prompt='Key', help='Your API key.')
@click.option('--secret', prompt='Secret', help='Your API secret.')
def login(key, secret):
    """Login with your API credentials.

      Prompts for input if key or secret are not passed as command line options.
    """

    auth.login(key, secret)
    click.echo('Credentials entered.')

@click.command()
def logout():
    """Clear your API credentials."""

    auth.logout()
    click.echo('Credentials cleared.')

@click.command()
@click.argument('input', metavar='URL')
@click.option('--format', 'format_', default='auto', show_default=True)
@click.option('--config', type=click.Path(exists=True))
@auth.pass_client
def pipe(client, input, format_, config):
    """Anonymise data on the fly.

      \b
      Read the INPUT data from a URL.
      Writes the anonymised data to stdout.

      Note that this parses, analyses and anonymises the data without
      persisting it. As a result, `pipe` is slower for repeated access
      than using `pull` to read previously ingested data.
    """

    path = '/redact/proxy'
    data = {'url': input_, 'format': format_}
    r = client.post(path, {'data': data})
    with click.open_file('-', mode='wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
            f.write(chunk)

@click.command()
@click.argument('input', metavar='INPUT_FILE_OR_URL')
@click.argument('name', metavar='RESOURCE_NAME') # XXX validate
@click.option('--format', 'format_', default='auto', show_default=True)
@auth.pass_client
def push(client, input, name, format_):
    """Ingest and store a data snapshot.

      \b
      Read the INPUT data from a local file PATH or a URL.
      Ingests it into a named RESOURCE.
    """

    if '://' in input:
        push_url(client, input, name, format_)
    else:
        push_file(client, input, name, format_)

def push_url(client, input_, name, format_):
    # First ingest.
    path = '/source/default/{0}'.format(name)
    data = {'url': input_, 'format': format_}
    r = client.post(path, {'data': data})
    # Then parse.
    path = '/parse/source/default/{0}'.format(name)
    r = client.post(path, {})
    click.secho(r.text, fg='green')

def push_file(client, input, name, format_):
    # First create an upload.
    path = '/source/default/{0}'.format(name)
    data = {'stream': True, 'format': format_}
    r = client.post(path, {'data': data})
    # Then stream the file up.
    path = r.json()['data']['path']
    with click.open_file(input, mode='rb') as f:
        r = client.upload(path, f)
    # Then parse.
    path = '/parse/source/default/{0}'.format(name)
    r = client.post(path, {})
    click.secho(r.text, fg='green')

@click.command()
@click.argument('name', metavar='RESOURCE_NAME') # XXX validate
@click.option('--config', type=click.Path(exists=True))
@auth.pass_client
def pull(client, name, config):
    """Get an anonymised data snapshot.

      \b
      Read from a named RESOURCE.
      Writes the anonymised data to stdout.
    """

    path = '/redact/source/default/{0}'.format(name)
    # XXX not dealing with the config yet
    data = {}
    r = client.post(path, data)
    with click.open_file('-', mode='wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
            f.write(chunk)

@click.group(cls=alias.AliasedGroup)
@click.option('--endpoint', metavar='URL', envvar='ANON_AI_ENDPOINT',
              default=DEFAULT_ENDPOINT, show_default=True,
              help='Web service API endpoint.')
@click.pass_context
def main(ctx, endpoint):
    """Anon AI :: Automatic data anonymisation using AI.

      Share data securely using a workflow tool that automatically anonymises
      and adapts to changing datasets.

      Run `anon COMMAND --help` for subcommand usage.
    """

    creds = auth.credentials()
    if creds:
        ctx.obj = client.Client(endpoint, *creds)
    else:
        is_login = 'login'.startswith(ctx.invoked_subcommand)
        is_help = sys.argv[-1] in ctx.help_option_names
        if not bool(is_login or is_help):
            msg = 'No credentials found. Do you need to login first?'
            click.secho(msg, fg='red')
            ctx.abort()

main.add_command(login)
main.add_command(logout)
main.add_command(pipe)
main.add_command(push)
main.add_command(pull)
