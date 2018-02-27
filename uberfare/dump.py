"""Contains interfaces to handle dumping of data to various storage mediums."""

import logging
from beautifultable import BeautifulTable
from csv import DictWriter, QUOTE_NONNUMERIC


def dump_to(method, raw_data, fields, **kwargs):
    """Dumps the data to an appropriate medium.

    :param method: either 'csv' or 'stdout'
    :param raw_data: list of dicts containing data from Uber's API
    :param fields: list of field names of the data to dump
    :param output_file: (optional) filename of the output when method: 'csv'
    """

    if method == 'csv':
        with CsvDumper(kwargs['output_file'], fields) as f:
            f.dump(raw_data)

    elif method == 'stdout':
        table_to_stdout(raw_data, fields)


class CsvDumper:
    """This class provides convenience to CSV dumping via Context Manager."""

    def __init__(self, filename, fieldnames, logger=None):

        #: filename for the output file where the data will be dumped
        self.filename = filename

        #: list of fieldnames that the CSV file will follow
        self.fieldnames = fieldnames

        #: file handle for writing to the output
        self.open_file = open(self.filename, 'a')

        #: :class:`DictWriter <DictWriter>` to handle writing dicts
        self.dict_writer = DictWriter(self.open_file, self.fieldnames,
                                      dialect='unix', quoting=QUOTE_NONNUMERIC)

        #: :class:`Logger <Logger>`
        self.logger = logger or logging.getLogger(__name__)

    def __enter__(self):
        self._write_csv_headers()
        return self

    def __exit__(self, *args):
        self.open_file.close()

    def _write_csv_headers(self):
        """Writes the CSV data headers into the file if it's still empty."""

        if self.open_file.tell() == 0:
            self.dict_writer.writeheader()

    def dump(self, list_of_dicts):
        """Dumps the list of dicts into the CSV file for this instance.

        :param list_of_dicts: As it says.
        """

        if len(list_of_dicts) == 0:
            return

        self.dict_writer.writerows(list_of_dicts)

        self.logger.info("Data collected and dumped: {}".format(self.filename))


def table_to_stdout(raw_data, fields, logger=None):
    """Logs the data in table-format using the logger.

    :param raw_data: list of dicts containing data from Uber's API
    :param fields: list of column names to filter the data with
    :param logger: (optional) overrides the default logger object
    """

    logger = logger or logging.getLogger(__name__)

    table = _make_data_table(raw_data, fields)

    logger.info('\n' + str(table) + '\n')


def _make_data_table(raw_data, display_fields):
    """Returns a table-formatted equivalent of the given data.

    :param raw_data: list of dicts containing data from Uber's API
    :param display_fields: list of column names to filter the data with
    :return: data in table form
    :rtype: :class:`BeautifulTable <BeautifulTable>`
    """

    table = BeautifulTable()

    data = {k: v for k, v in _transpose_to_columnar(raw_data).items()
            if k in display_fields}

    for header_name in display_fields:
        table.append_column(header_name, data[header_name])

    return table


def _transpose_to_columnar(raw_data):
    """Groups the same data together by key.

    BEFORE:
        [
            { 'product': 'apple', 'price': 10.0 },
            { 'product': 'banana', 'price': 5.0 }
        ]

    AFTER:
        {
            'product': ['apple', 'banana'],
            'price': [10.0, 5.0],
        }

    :param raw_data: list of dictionaries
    :return: dictionary where keys are the column names
    :rtype: dict
    """

    columnar_data = {}

    for entry in raw_data:
        for key, val in entry.items():
            if key not in columnar_data:
                columnar_data[key] = []
            columnar_data[key].append(val)

    return columnar_data
