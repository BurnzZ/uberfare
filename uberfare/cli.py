"""Establishes the interface for the Command Line."""

import click
import re
from .core import fare_estimate
from .environments import UBER_SERVER_TOKEN


def validate_coordinate(ctx, param, value):
    """Ensures the passed parameter is formatted: <LATITUDE>,<LONGITUDE>"""

    if not re.match(r'\d+(\.\d+)?,\d+(\.\d+)?', value):
        raise click.BadParameter('Coordinates must be in the format: '
                                 '123.23,42.1')
    return value


@click.group()
@click.option('--check-interval', default=0, help='Set the time interval in '
              'seconds to periodically check the Uber fares. If this isn\'t '
              'set, the script would simply request once to the Uber API.')
@click.option('--server-token', help='Server Token to function as API KEY. '
              'When set, this overrides the env value in $UBER_SERVER_TOKEN.')
@click.pass_context
def cli(ctx, server_token, check_interval):
    """Uberfare provides CLI-access to the Uber SDK for collecting fares.

    It currently supports the fare 'estimate' where a price range (low, high)
    is provided instead of the exact fare. Requesting the fare 'estimate' only
    needs the SERVER Token as the API access.

    On the otherhand, the 'upfront' fare requires OAUTH2 access and currently
    isn't supported, but probably in the near future.
    """
    ctx.obj = {}
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