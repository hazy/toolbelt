"""Hazy command line interface.

  Run `hazy --help` for usage.
"""

import click

DEFAULT_ENDPOINT="https://api.hazy.com"

@click.group() # cls=alias.AliasedGroup
@click.option('--endpoint', metavar='URL', envvar='HAZY_ENDPOINT',
              default=DEFAULT_ENDPOINT, show_default=True,
              help='Web service API endpoint.')
@click.pass_context
def main(ctx, endpoint):
    """Hazy - Treat data responsibly."""

    click.secho("NotImplemented", fg='red')
    ctx.abort()

if __name__ == '__main__':
    main()

# https://devcenter.heroku.com/articles/authentication
