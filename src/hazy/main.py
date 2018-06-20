"""Hazy command line interface.

  Run `hazy --help` for usage.
"""

import click

from . import aliased

from .resources.auth import auth
from .resources.entity import entity
from .resources.policy import policy
from .resources.source import source

DEFAULT_ENDPOINT="https://api.hazy.com"

@click.group(cls=aliased.Group, section_label='Resources')
@click.option('--endpoint', metavar='URL', envvar='HAZY_ENDPOINT',
              default=DEFAULT_ENDPOINT, show_default=True,
              help='Web service API endpoint.')
@click.pass_context
def cli(ctx, endpoint):
    """Hazy - Treat data responsibly."""

    # https://devcenter.heroku.com/articles/authentication
    ctx.obj = NotImplemented

@cli.command()
@click.pass_obj
def docs(obj):
    """Open the online documentation in a web browser."""

    raise NotImplementedError

cli.add_command(auth)
cli.add_command(entity)
cli.add_command(source)
cli.add_command(policy)
