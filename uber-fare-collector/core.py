from collections import namedtuple
from time import sleep
from datetime import datetime
from csv import DictWriter
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

Coordinates = namedtuple('Coordinates', ['start_latitude', 'start_longitude',
                                         'end_latitude', 'end_longitude'])


def get_read_only_client(api_key):
    """Returns an Uber client only capable of accessing Read-Only resource.

    Examples of Read-Only resources are 'products available in an area' and
    'fare estimates'.
    """

    session = Session(server_token=api_key)
    return UberRidesClient(session)


def _tokenizer(data):
    return [token.strip() for token in data.split(',')]


def create_coordinates(origin, dest):

    origin_tok = _tokenizer(origin)
    dest_tok = _tokenizer(dest)

    return Coordinates(origin_tok[0], origin_tok[1],
                       dest_tok[0], dest_tok[1])


def write_to_csv(list_of_dicts, output_file):

    if len(list_of_dicts) == 0:
        return

    timestamp = datetime.now().isoformat()

    for d in list_of_dicts:
        d.update({'timestamp': timestamp})

    with open(output_file, 'a') as f:
        dict_writer = DictWriter(f, list_of_dicts[0].keys())
        dict_writer.writerows(list_of_dicts)


def collector(client, coordinates):

    return client.get_price_estimates(
        start_latitude=coordinates.start_latitude,
        start_longitude=coordinates.start_longitude,
        end_latitude=coordinates.end_latitude,
        end_longitude=coordinates.end_longitude
    )


def fare_estimate(api_key, origin, dest, output_file, check_interval):

    client = get_read_only_client(api_key)
    coordinates = create_coordinates(origin, dest)

    while True:
        raw_data = collector(client, coordinates)
        print(raw_data.json)

        write_to_csv(raw_data.json['prices'], output_file)

        sleep(check_interval)
