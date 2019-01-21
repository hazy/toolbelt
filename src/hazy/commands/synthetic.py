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

    Example:
    `hazy synthetic list`
    '''

@synthetic.command()
@click.argument('uuid')
def show(uuid):
    '''View a Synthetic Data associated with your account.


    Example:
    `hazy synthetic show 2bcac5e8-fc4e-4675-ae58-c4b67b552888`
    '''

@synthetic.command()
@click.argument('uuid')
def rm(uuid):
    '''Remove the Synthetic Data identified by the given UUID.

    All Synthetic Data generated and associated with your account have an unique ID.
    You can view this ID by when you list all synthetic data in your account using the
    command `hazy synthetic list`. You can then use this unique ID to remove a particular
    Synthetic Data from your account.

    Example:
    `hazy synthetic rm 2bcac5e8-fc4e-4675-ae58-c4b67b552888`
    '''
