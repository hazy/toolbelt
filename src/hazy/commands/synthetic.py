"""Sub command to manage synthetic data associated with your account.

  Run `hazy synthetic --help` for usage.
"""

import click

@click.group()
def synthetic():
    '''Manage Synthetic Data associated with your account.
    '''

@synthetic.command()
def list():
    '''Lists all Synthetic Data associated with your account.
    '''

@synthetic.command()
def show():
    '''View a Synthetic Data associated with your account.
    '''

@synthetic.command()
def rm():
    '''Remove a Synthetic Data associated with your account.
    '''
