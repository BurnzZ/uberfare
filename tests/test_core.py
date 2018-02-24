import unittest.mock as mock
import uber_fare_collector.core as core


@mock.patch('uber_fare_collector.core.UberRidesClient')
@mock.patch('uber_fare_collector.core.Session')
def test_get_read_only_client(mock_session, mock_client):
    """It should correctly call the Uber Session and pass it to the Client."""

    core.get_read_only_client('APIKEY123')

    mock_session.assert_called_once_with(server_token='APIKEY123')
    mock_client.assert_called_once_with(mock_session())


def test_create_coordinates():
    """It should return an instance of Coordinates with correct attributes."""

    origin = '142.23,12.3'
    dest = '3.3,4.4'

    result = core.create_coordinates(origin, dest)

    assert isinstance(result, core.Coordinates)
    assert result.start_latitude == '142.23'
    assert result.start_longitude == '12.3'
    assert result.end_latitude == '3.3'
    assert result.end_longitude == '4.4'


@mock.patch('uber_fare_collector.core.datetime')
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


@mock.patch('uber_fare_collector.core.DictWriter')
def test_write_to_csv(mock_dictwriter):
    """It should write the data in CSV format with an additional timestamp."""

    data = [
        {'arg': 't1', 'val': 'x', 'timestamp': '2018-02-19T15:19:39.137995'},
        {'arg': 't2', 'val': 'y', 'timestamp': '2018-02-19T15:19:39.137995'}
    ]
    output_file = 'test-out.csv'

    m = mock.mock_open()
    with mock.patch('uber_fare_collector.core.open', m):
        core.write_to_csv(data, output_file)

        m.assert_called_once_with(output_file, 'a')

        mock_dictwriter.assert_called_once_with(m(), data[0].keys())
        mock_dictwriter().writerows.assert_called_once_with(data)


def test_collect_price():
    """It should call the correct method of the passed client using the passed
    coordinates value."""

    mock_client = mock.Mock()
    mock_client.get_price_estimates.return_value.json = {
            'prices': 'this should be returned'}

    coordinates = core.Coordinates(1, 2, 3, 4)
    result = core.collect_price(mock_client, coordinates)

    mock_client.get_price_estimates.assert_called_once_with(
        start_latitude=coordinates.start_latitude,
        start_longitude=coordinates.start_longitude,
        end_latitude=coordinates.end_latitude,
        end_longitude=coordinates.end_longitude
    )

    assert result == 'this should be returned'


def test_fare_estimate():
    pass
