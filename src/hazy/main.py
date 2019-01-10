"""Hazy command line interface.

"""

import click

from .commands.auth import auth
from .commands.db import db
from .commands.generator import generator
from .commands.synthetic import synthetic

@click.group()
def cli():
    '''Hazy toolbelt - Unlock data innovation!
    '''

cli.add_command(auth)
cli.add_command(db)
cli.add_command(generator)
cli.add_command(synthetic)
