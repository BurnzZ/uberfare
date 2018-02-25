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
