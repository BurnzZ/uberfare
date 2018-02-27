"""Establishes the interface for the Command Line."""

import click
import logging
import re
from .core import fare_estimate
from .environments import UBER_SERVER_TOKEN

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')


def validate_coordinate(ctx, param, value):
    """Ensures the passed parameter is formatted: <LATITUDE>,<LONGITUDE>"""

    if not re.match(r'\d+(\.\d+)?,\d+(\.\d+)?', value):
        raise click.BadParameter('Coordinates must be in the format: '
                                 '123.23,42.1 <LATITUDE,LONGITUDE>')
    return value


@click.group()
@click.option('--check-interval', '-ci', default=0, help='Interval in seconds '
              'to periodically check the Uber fares. If this isn\'t set, the '
              'script would simply request once to the Uber API.')
@click.option('--server-token', '-st', help='Server Token used as an API KEY. '
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
@click.option('--output-file', '-o', help='Write the RAW output to the given '
              'output filepath in a CSV format (instead of simply STDOUT).')
@click.pass_obj
def estimate(ctx, origin, destination, output_file):
    """Retrieves the Uber fare estimates from <origin> to <dest> on STDOUT.

    The <origin> and <dest> values must be in the format: LATITUDE,LONGITUDE.

    If --check-interval isn't set, this would only fetch to the API once.
    You can also write the raw data coming from the server into a *.csv file
    via the --output-file flag.
    """

    fare_estimate(ctx['SERVER_TOKEN'], origin, destination, output_file,
                  ctx['CHECK_INTERVAL'])
