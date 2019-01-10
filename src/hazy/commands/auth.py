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
    '''

@auth.command()
def logout():
    '''Logout and remove all stored credentials
    '''
