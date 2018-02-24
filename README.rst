Overview
========

This is a simple wrapper to the official Uber Python SDK intended to
collect data from a given **origin** and **destination** at a specified
time interval.

The current implementation only handles the price estimate feature since
it doesn’t need OAuth 2.0 access.

Motivation
~~~~~~~~~~

I’m using this tool in order to gather data and then evaluate when’s the
best time to leave the house and book an Uber ride to work, and
vice-versa.

API Key
~~~~~~~

Get your ``Server Token`` API Key by creating an app at:
`developer.uber.com/dashboard <https://developer.uber.com/dashboard>`__

Before using this package, export your ``Server Token`` as:
``export UBER_SERVER_TOKEN=<Server Token>``. You can however, override
this when using the CLI (see below).

Usage
~~~~~

You have to determine the ``(latitude,longitude)`` of your location,
since the types of rides available will depend on it.

The best way to get the coordinates is going to
`maps.google.com <https://www.google.com.ph/maps>`__ and then clicking
any point in the map. A small box will then appear at the bottom-center
of your screen containing the Longitude and Latitude. Take note of the
coordinates for both your origin and destination:

.. figure:: docs/img/google-maps-coordinate-lookup.gif
   :alt: Google Maps Coordinates Lookup

   Google Maps Coordinates Lookup

CLI
^^^

.. code:: bash

    >>> # To get the fare estimate, provide the arguments: origin, destination, output-file path
    >>> # Where origin and destination are in the LATITUDE,LONGITUDE format
    >>> uberfare estimate 14.55,121.05 14.52,121.01 output.csv

    >>> # You can override the default check interval of 120 seconds via:
    >>> uberfare --check-interval 5 estimate 14.55,121.05 14.52,121.01 output.csv

    >>> # You can override the 'UBER_SERVER_TOKEN' env variable in the CLI via:
    >>> uberfare --server_token <SERVER API KEY> estimate 14.55,121.05 14.52,121.01 output.csv

Notes
~~~~~

Be careful when specifying a very short time interval for checking the
price since you might be rate limited.

Future Releases
~~~~~~~~~~~~~~~

-  Better interface for importing as a package
-  Support the Upfront Fare data collection by enabling the OAUTH2.
