from collections import namedtuple
from csv import DictWriter
from datetime import datetime
from time import sleep
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


def create_coordinates(origin, dest):

    def tokenizer(data):
        return [token.strip() for token in data.split(',')]

    origin_tokens = tokenizer(origin)
    dest_tokens = tokenizer(dest)

    return Coordinates(origin_tokens[0], origin_tokens[1],
                       dest_tokens[0], dest_tokens[1])


def add_timestamp(list_of_dicts):

    timestamp = datetime.now().isoformat()

    for d in list_of_dicts:
        d.update({'timestamp': timestamp})

    return list_of_dicts


def write_to_csv(list_of_dicts, output_file):

    if len(list_of_dicts) == 0:
        return

    with open(output_file, 'a') as f:
        dict_writer = DictWriter(f, list_of_dicts[0].keys())
        dict_writer.writerows(list_of_dicts)

    print("{} | Data collected: {}".format(datetime.now().isoformat(),
          output_file))


def collect_price(client, coordinates):

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
