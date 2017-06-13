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
@click.argument('input', metavar='INPUT_PATH_OR_URL')
@click.argument('output', metavar='OUTPUT_PATH', type=click.Path())
@click.option('--format', 'format_', default='auto', show_default=True)
@click.option('--config', type=click.Path(exists=True))
@auth.pass_client
def pipe(client, input, output, format_, config):
    """Anonymise data on the fly.

      \b
      Read the INPUT data from a local file PATH or a URL.
      OUTPUT the anonymised data to a local file PATH.

      Note that this parses, analyses and anonymises the data without
      persisting it. As a result, `pipe` is slower for repeated access
      than using `pull` to read previously ingested data.
    """

    if '://' in input:
        pipe_url(client, input, output, format_, config)
    else:
        pipe_file(client, input, output, format_, config)

def pipe_url(client, input_, output, format_, config):
    path = '/redact/proxy'
    data = {'url': input_, 'format': format_}
    r = client.post(path, {'data': data})
    with click.open_file(output, mode='wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
            f.write(chunk)

def pipe_file(*args):
    raise NotImplementedError

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
