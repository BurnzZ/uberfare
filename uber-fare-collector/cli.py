"""Establishes the interface for the Command Line."""

import re
import click
from environments import UBER_SERVER_TOKEN
from core import fare_estimate


def validate_coordinate(ctx, param, value):
    """Ensures the passed parameter is formatted: <LATITUDE>,<LONGITUDE>"""

    if not re.match(r'\d+(\.\d+)?,\d+(\.\d+)?', value):
        raise click.BadParameter('Coordinates must be in the format: '
                                 '123.23,42.1')
    return value


@click.group()
@click.option('--check-interval', default=120)
@click.option('--server-token')
@click.pass_context
def cli(ctx, server_token, check_interval):
    ctx.obj['SERVER_TOKEN'] = server_token or UBER_SERVER_TOKEN
    ctx.obj['CHECK_INTERVAL'] = check_interval


@cli.command()
@click.argument('origin', callback=validate_coordinate)
@click.argument('destination', callback=validate_coordinate)
@click.argument('output-file')
@click.pass_obj
def estimate(ctx, origin, destination, output_file):
    fare_estimate(ctx['SERVER_TOKEN'], origin, destination, output_file,
                  ctx['CHECK_INTERVAL'])


if __name__ == '__main__':
    cli(obj={})
