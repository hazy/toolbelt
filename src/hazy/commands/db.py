"""Sub command to manage database connections associated with your account.

  Run `hazy db --help` for usage.
"""

import click


@click.group()
def db():
    '''Manage database connections associated with your account.
    '''

@db.command()
def add():
    '''Add a new database connection detail.
    '''

@db.command()
def rm():
    '''Remove a database connection detail.
    '''

@db.command()
def list():
    '''List all database connection details with your account.
    '''

@db.command()
def tables_list():
    '''List all tables of a database.
    '''
