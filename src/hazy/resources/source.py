"""Sub command to manage data sources.

  Run `hazy source --help` for usage.
"""

import click

from .. import aliased

@click.group(cls=aliased.Group)
@click.pass_obj
def source(obj):
    """Connect and manage data sources."""

@source.command()
@click.pass_obj
def create(obj):
    """Create a data source."""
