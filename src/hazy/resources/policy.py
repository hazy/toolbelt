"""Sub command to manage sharing policies.

  Run `hazy policy --help` for usage.
"""

import click

from .. import aliased

@click.group(cls=aliased.Group)
@click.pass_obj
def policy(obj):
    """Manage data sharing policies and legal terms."""

@policy.command()
@click.pass_obj
def create(obj):
    """Create a sharing policy."""
