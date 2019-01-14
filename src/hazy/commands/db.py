"""Sub command to manage database connections associated with your account.

  Run `hazy db --help` for usage.
"""

import click

@click.group()
def db():
    '''Manage database connections associated with your account.
    '''

@db.command()
@click.option('-h', '--host', required=True)
@click.option('-u', '--user', required=True)
@click.option('-p', '--password', required=True)
@click.option('-db', '--database', required=True)
def add(host, user, password, database):
    '''Add a new database connection detail.

    Example:
    hazy db add --host host --user user --pass pass --db db
    '''
    click.echo(host)

@db.command()
@click.argument('uuid')
def rm(uuid):
    '''Remove a database connection detail.

    Example:
    hazy db rm 2bcac5e8-fc4e-4675-ae58-c4b67b552888
    '''

@db.command()
def list():
    '''List all database connection details with your account.

    Example:
    hazy db list
    '''

@db.command()
@click.argument('uuid')
def list_tables(uuid):
    '''List all tables of a database.

    Example:
    hazy db list-tables 2bcac5e8-fc4e-4675-ae58-c4b67b552888
    '''
