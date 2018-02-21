"""Anon AI command line interface.

  Run `anon --help` for usage.
"""

import base64
import click
import json
import math
import sys

from . import alias
from . import auth
from . import client
from . import util

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
@click.argument('input', metavar='FILE_OR_URL')
@click.argument('name', metavar='RESOURCE_NAME') # XXX validate
@click.option('--encryption-key', metavar='LONG_RANDOM_STRING')
@click.option('--format', 'format_', default='text', show_default=True) # default='auto'
@auth.pass_client
def push(client, input, name, encryption_key, format_):
    """Ingest and store a data snapshot.

      \b
      Read the input data from a local file path or a URL.
      Ingests it into a named RESOURCE.
    """

    data = {'format': format_}
    if encryption_key:
        data['encryption_key'] = util.encode_key(encryption_key)
    if '://' in input:
        push_url(client, input, name, data)
    else:
        push_file(client, input, name, data)

def push_url(client, url, name, data):
    # First ingest.
    data['url'] = url
    path = '/source/default/{0}'.format(name)
    r = client.post(path, {'data': data})
    # Then parse.
    path = '/parse/source/default/{0}'.format(name)
    r = client.post(path, {})
    click.secho(r.text, fg='green')

def push_file(client, file_, name, data):
    # First create an upload.
    data['stream'] = True
    path = '/source/default/{0}'.format(name)
    r = client.post(path, {'data': data})
    # Then stream the file up.
    r_data = r.json()['data']
    path = r_data['path']
    datakey = base64.b64decode(r_data['datakey'])
    with click.open_file(file_, mode='rb') as f:
        r = client.upload(path, f, datakey, data.get('encryption_key'))
        # print(r.json())
    # Then parse.
    path = '/parse/source/default/{0}'.format(name)
    r = client.post(path, {'data': data})
    click.secho(r.text, fg='green')

@click.command()
@click.argument('name', metavar='RESOURCE_NAME') # XXX validate
@click.option('--config', type=click.File())
@click.option('--encryption-key', metavar='LONG_RANDOM_STRING')
@auth.pass_client
def pull(client, name, config, encryption_key):
    """Get an anonymised data snapshot.

      \b
      Read from a named RESOURCE.
      Writes the anonymised data to stdout.
    """

    path = '/redact/source/default/{0}'.format(name)
    data = {}
    if config:
        try:
            data['config'] = json.loads(config.read())
        except Exception as err:
            msg = 'Invalid config. {0}.'.format(err)
            click.secho(msg, fg='red')
            return
    if encryption_key:
        data['encryption_key'] = util.encode_key(encryption_key)
    r = client.post(path, {'data': data})
    with click.open_file('-', mode='wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
            f.write(chunk)

@click.command()
@click.argument('url', metavar='URL')
@click.option('--format', 'format_', default='text', show_default=True) # default='auto'
@click.option('--config', type=click.File())
@auth.pass_client
def pipe(client, url, format_, config):
    """Anonymise data on the fly.

      \b
      Input from URL only (see `push` for local file support).
      Writes the anonymised data to stdout.

      Note that this parses, analyses and anonymises the data without
      persisting it. As a result, `pipe` is slower for repeated access
      than using `push` and `pull` to read previously ingested data.
    """

    path = '/redact/proxy'
    data = {'url': url, 'format': format_}
    if config:
        try:
            data['config'] = json.loads(config.read())
        except Exception as err:
            msg = 'Invalid config. {0}.'.format(err)
            click.secho(msg, fg='red')
            ctx.abort()
    r = client.post(path, {'data': data})
    with click.open_file('-', mode='wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
            f.write(chunk)

@click.group(cls=alias.AliasedGroup)
@click.option('--endpoint', metavar='URL', envvar='ANON_AI_ENDPOINT',
              default=DEFAULT_ENDPOINT, show_default=True,
              help='Web service API endpoint.')
@click.pass_context
def main(ctx, endpoint):
    """Anon AI :: Automated data anonymisation using AI.

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
main.add_command(push)
main.add_command(pull)
main.add_command(pipe)
