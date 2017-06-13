"""Anon AI command line interface.

  Run `anon --help` for usage.
"""

import click

from . import auth
from . import client

DEFAULT_ENDPOINT="https://backend.redact.at"

@click.command()
@click.option('--key', prompt='Key', help='Your API key.')
@click.option('--secret', prompt='Secret', help='Your API secret.')
def login(key, secret):
    auth.login(key, secret)
    click.echo('Credentials updated.')

@click.group()
@click.option('--endpoint', envvar='ANON_AI_ENDPOINT', default=DEFAULT_ENDPOINT)
@click.pass_context
def main(ctx, endpoint):
    creds = auth.credentials()
    if creds:
        ctx.obj = client.Client(endpoint, *creds)
    elif ctx.invoked_subcommand != 'login':
        raise click.UsageError("No credentials found. Do you need to login first?")

main.add_command(login)
