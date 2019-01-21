"""Sub command to manage authentication.

  Run `hazy source --help` for usage.
"""

import click

@click.group()
def auth():
    '''Authenticate with Hazy
    '''

@auth.command()
def login():
    '''Login in to use Hazy toolbelt

    Example:
    `hazy auth login --email email --pass pass`
    '''

@auth.command()
def logout():
    '''Logout and remove all stored credentials

    Example:
    `hazy auth logout`
    '''
