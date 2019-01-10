"""Sub command to manage trained generators associated with your account.

  Run `hazy generator --help` for usage.
"""

import click

@click.group()
def generator():
    '''Manage trained generators associated with your account.
    '''

@generator.command()
def train():
    '''Train a new generator with your data.
    '''

@generator.command()
def list():
    '''List the trained generators in your account.
    '''

@generator.command()
def show():
    '''View details of a single trained generator.
    '''

@generator.command()
def jobs():
    '''View all synthetic data jobs of a generator.
    '''
