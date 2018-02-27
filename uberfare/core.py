from collections import namedtuple
from copy import deepcopy
from datetime import datetime
from time import sleep
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from .dump import dump_to
from .fields import ESTIMATE_CSV_FIELDS, ESTIMATE_STDOUT_FIELDS

Coordinates = namedtuple('Coordinates', ['start_latitude', 'start_longitude',
                                         'end_latitude', 'end_longitude'])


def get_read_only_client(api_key):
    """Returns an UberRidesClient only capable of accessing Read-Only resource.

    Examples of Read-Only resources are 'products available in an area' and
    'fare estimates'.

    :param api_key: string SERVER token.
    :return: :class:`UberRidesClient <UberRidesClient>` object
    :rtype: uber_rides.client.UberRidesClient
    """

    session = Session(server_token=api_key)
    return UberRidesClient(session)


def create_coordinates(origin, dest):
    """Returns a Coordinates namedtuple using the origin and dest tuples.

    :param origin: string formatted as 'LATITUDE,LONGITUDE'.
    :param dest: string formatted as 'LATITUDE,LONGITUDE'.
    :return: :class:`Coordinates <Coordinates>` object
    :rtype: namedtuple
    """

    def tokenizer(data):
        return [token.strip() for token in data.split(',')]

    origin_tokens = tokenizer(origin)
    dest_tokens = tokenizer(dest)

    return Coordinates(origin_tokens[0], origin_tokens[1],
                       dest_tokens[0], dest_tokens[1])


def add_timestamp(list_of_dicts):
    """Returns a new list of dicts with a new a timestamp entry.

    This function avoids modifying the passed list by creating a deepcopy.

    :param list_of_dicts: As it says.
    :return: list of dicts
    """

    timestamp = {'timestamp': datetime.now().isoformat()}

    list_copy = deepcopy(list_of_dicts)

    for d in list_copy:
        d.update(timestamp)

    return list_copy


def get_price_estimate(client, coordinates):
    """Returns the price estimate data for the given `coordinates`.

    :param client: :class:`UberRidesClient <UberRidesClient>` object.
    :param client: :class:`Coordinates <Coordinates>` object.
    :return: price estimate data
    :rtype: list of dictionaries
    """

    return client.get_price_estimates(
        start_latitude=coordinates.start_latitude,
        start_longitude=coordinates.start_longitude,
        end_latitude=coordinates.end_latitude,
        end_longitude=coordinates.end_longitude
    ).json['prices']


def fare_estimate(api_key, origin, dest, output_file=None, check_interval=0):
    """Fetches the fare estimate data and logs it to either CSV file or STDOUT.

    :param api_key: string SERVER token.
    :param origin: string formatted as 'LATITUDE,LONGITUDE'.
    :param dest: string formatted as 'LATITUDE,LONGITUDE'.
    :param output_file: (optional) string filename where the data will be
        written. If omitted, the data will be logged into STDOUT.
    :param check_interval: (optional) integer time in seconds between each API
        call. If omitted, this would only result to one (1) fetch.
    """

    client = get_read_only_client(api_key)
    coordinates = create_coordinates(origin, dest)

    while True:
        raw_data = get_price_estimate(client, coordinates)

        if output_file:
            timestampped_data = add_timestamp(raw_data)
            dump_to('csv', timestampped_data, output_file=output_file,
                    fields=ESTIMATE_CSV_FIELDS)
        else:
            dump_to('stdout', raw_data, fields=ESTIMATE_STDOUT_FIELDS)

        if not check_interval:
            return

        sleep(check_interval)
