import os
from collections import namedtuple
import unittest.mock as mock
import uberfare.core as core


@mock.patch('uberfare.core.UberRidesClient')
@mock.patch('uberfare.core.Session')
def test_get_read_only_client(mock_session, mock_client):
    """It should correctly call the Uber Session and pass it to the Client."""

    core.get_read_only_client('APIKEY123')

    mock_session.assert_called_once_with(server_token='APIKEY123')
    mock_client.assert_called_once_with(mock_session())


def test_create_coordinates():
    """It should return a Coordinates instance with correct attributes."""

    origin = '142.23,12.3'
    dest = '3.3,4.4'

    result = core.create_coordinates(origin, dest)

    assert isinstance(result, core.Coordinates)
    assert result.start_latitude == '142.23'
    assert result.start_longitude == '12.3'
    assert result.end_latitude == '3.3'
    assert result.end_longitude == '4.4'


@mock.patch('uberfare.core.datetime')
def test_add_timestamp(mock_datetime):
    """It should return a new list of dicts with a timestamp in each entry."""

    mock_datetime.now().isoformat.return_value = 'T123'

    list_of_dicts = [{'key1': 1}, {'key2': 2}]

    result = core.add_timestamp(list_of_dicts)

    assert result == [
        {'key1': 1, 'timestamp': 'T123'},
        {'key2': 2, 'timestamp': 'T123'}
    ]

    assert result != list_of_dicts


def test_get_price_estimate():
    """It should call the correct method of the passed client using the passed
    coordinates value."""

    mock_client = mock.Mock()
    mock_client.get_price_estimates.return_value.json = {
            'prices': 'this should be returned'}

    coordinates = core.Coordinates(1, 2, 3, 4)
    result = core.get_price_estimate(mock_client, coordinates)

    mock_client.get_price_estimates.assert_called_once_with(
        start_latitude=coordinates.start_latitude,
        start_longitude=coordinates.start_longitude,
        end_latitude=coordinates.end_latitude,
        end_longitude=coordinates.end_longitude
    )

    assert result == 'this should be returned'


class FakeUberRidesClient:
    """Replacing the actual client to have controlled outputs."""

    def __init__(self, session):
        self.session = session

    def get_price_estimates(*args, **kwargs):

        Response = namedtuple('Response', ['json'])

        return Response(
            {'prices': [
                {
                    'localized_display_name': 'uberX',
                    'distance': 5.15,
                    'display_name': 'uberX',
                    'product_id': 'ID1-WWWW-XXXX-YYYY-ZZZZZZZZZZZZ',
                    'high_estimate': 250.0,
                    'low_estimate': 204.0,
                    'duration': 1020,
                    'estimate': 'PHP204-250',
                    'currency_code': 'PHP'
                }, {
                    'localized_display_name': 'uberPOOL',
                    'distance': 5.15,
                    'display_name': 'uberPOOL',
                    'product_id': 'ID2-WWWW-XXXX-YYYY-ZZZZZZZZZZZZ',
                    'high_estimate': 169.0,
                    'low_estimate': 136.0,
                    'duration': 1020,
                    'estimate': 'PHP136-168',
                    'currency_code': 'PHP'
                }, {
                    'localized_display_name': 'uberXL',
                    'distance': 5.15,
                    'display_name': 'uberXL',
                    'product_id': 'ID3-WWWW-XXXX-YYYY-ZZZZZZZZZZZZ',
                    'high_estimate': 376.0,
                    'low_estimate': 306.0,
                    'duration': 1020,
                    'estimate': 'PHP306-376',
                    'currency_code': 'PHP'
                }, {
                    'localized_display_name': 'uberBLACK',
                    'distance': 5.15,
                    'display_name': 'uberBLACK',
                    'product_id': 'ID4-WWWW-XXXX-YYYY-ZZZZZZZZZZZZ',
                    'high_estimate': 291.0,
                    'low_estimate': 237.0,
                    'duration': 1020,
                    'estimate': 'PHP237-291',
                    'currency_code': 'PHP'
                }
            ]}
        )


@mock.patch('uberfare.core.datetime')
def test_fare_estimate(mock_datetime, tmpdir):
    """It should produce the correct output file."""

    # NOTE: used the patch() as context manager since pytest doesn't work well
    #   with its fixtures if more than one (1) mock decorator is used.

    with mock.patch('uberfare.core.UberRidesClient', new=FakeUberRidesClient):

        mock_datetime.now().isoformat.return_value = 'T123'

        this_dir = os.path.abspath(os.path.dirname(__file__))
        expected_file = os.path.join(this_dir, 'artifacts', 'expected_out.csv')

        output_file = tmpdir.join('out.csv')

        core.fare_estimate('API123', '12,34', '56,78', str(output_file), 0)

        with open(expected_file) as f:
            assert output_file.read() == f.read()
