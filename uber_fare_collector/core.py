from collections import namedtuple
from copy import deepcopy
from csv import DictWriter
from datetime import datetime
from time import sleep
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

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

    :param origin: tuple formatted as (latitude, longitude).
    :param dest: tuple formatted as (latitude, longitude).
    :return: Coordinates object
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


def write_to_csv(list_of_dicts, output_file):
    """Writes the given list of dicts into the provided output file path.

    This assumes that each dictionary in the list has the same keys.

    :param list_of_dicts: As it says.
    :param output_file: string denoting the file to be created.
    """

    if len(list_of_dicts) == 0:
        return

    with open(output_file, 'w') as f:
        dict_writer = DictWriter(f, list_of_dicts[0].keys())
        dict_writer.writerows(list_of_dicts)

    print("{} | Data collected: {}".format(datetime.now().isoformat(),
          output_file))


def collect_price(client, coordinates):
    """Returns the price estimate data using the given client.

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


def fare_estimate(api_key, origin, dest, output_file, check_interval):

    client = get_read_only_client(api_key)
    coordinates = create_coordinates(origin, dest)

    while True:
        raw_data = collect_price(client, coordinates)
        data = add_timestamp(raw_data)
        write_to_csv(data, output_file)
        sleep(check_interval)
