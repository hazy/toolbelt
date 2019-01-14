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

    Example:
    hazy generator train --db 2bcac5e8-fc4e-4675-ae58-c4b67b552888 --table table
    '''

@generator.command()
def list():
    '''List the trained generators in your account.

    Example:
    `hazy generator list`
    '''

@generator.command()
@click.argument('uuid')
def show(uuid):
    '''View details of a single trained generator.

    Example:
    `hazy generator show 2bcac5e8-fc4e-4675-ae58-c4b67b552888`
    '''

@generator.command()
@click.argument('uuid')
def jobs(uuid):
    '''View all synthetic data jobs of a generator.

    Example:
    `hazy generator jobs 2bcac5e8-fc4e-4675-ae58-c4b67b552888`
    '''
