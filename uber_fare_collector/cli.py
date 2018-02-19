"""Establishes the interface for the Command Line."""

import re
import click
from .environments import UBER_SERVER_TOKEN
from .core import fare_estimate


def validate_coordinate(ctx, param, value):
    """Ensures the passed parameter is formatted: <LATITUDE>,<LONGITUDE>"""

    if not re.match(r'\d+(\.\d+)?,\d+(\.\d+)?', value):
        raise click.BadParameter('Coordinates must be in the format: '
                                 '123.23,42.1')
    return value


@click.group()
@click.option('--check-interval', default=120, help='Time Interval in seconds '
        'to check the Uber fares. Default: 120.')
@click.option('--server-token', help='Server Token to function as API KEY. '
        'Default: <env var: $UBER_SERVER_TOKEN>')
@click.pass_context
def cli(ctx, server_token, check_interval):
    ctx.obj['SERVER_TOKEN'] = server_token or UBER_SERVER_TOKEN
    ctx.obj['CHECK_INTERVAL'] = check_interval


@cli.command(short_help='retrieves the Uber fare estimates.')
@click.argument('origin', callback=validate_coordinate, metavar='<origin>')
@click.argument('destination', callback=validate_coordinate, metavar='<dest>')
@click.argument('output-file', metavar='<output file>')
@click.pass_obj
def estimate(ctx, origin, destination, output_file):
    """This periodically retrieves the Uber fare esimates from <origin>
    to <dest>."""

    fare_estimate(ctx['SERVER_TOKEN'], origin, destination, output_file,
                  ctx['CHECK_INTERVAL'])


if __name__ == '__main__':
    cli(obj={})
