pynmea2
=======

`pynmea2` is a python library for the [NMEA 0183](http://en.wikipedia.org/wiki/NMEA_0183) protocol

`pynmea2` is based on [`pynmea`](https://code.google.com/p/pynmea/) by Becky Lewis

The `pynmea2` homepage is located at http://github.com/Knio/pynmea2


### Compatibility

`pynmea2` is compatable with Python 2.7 and Python 3.3

[![Build Status](https://travis-ci.org/Knio/pynmea2.png?branch=master)](https://travis-ci.org/Knio/pynmea2)
[![Coverage Status](https://coveralls.io/repos/Knio/pynmea2/badge.png?branch=master)](https://coveralls.io/r/Knio/pynmea2?branch=master)

### Installation

The recommended way to install `pynmea2` is with
[pip](http://pypi.python.org/pypi/pip/):

    pip install pynmea2

[![PyPI version](https://badge.fury.io/py/pynmea2.png)](http://badge.fury.io/py/pynmea2)

Parsing
-------

You can parse individual NMEA sentences using the `parse()` function, which takes a string containing a
NMEA 0183 sentence and returns a `NMEASentence` object. Note that the leading '$' is optional and trailing whitespace is ignored when parsing a sentence.

Example:

    >>> import pynmea2
    >>> msg = pynmea2.parse("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D")
    >>> msg
    <GGA(timestamp=datetime.time(18, 43, 53), lat='1929.045', lat_dir='S', lon='02410.506', lon_dir='E', gps_qual='1', num_sats='04', horizontal_dil='2.6', altitude=100.0, altitude_units='M', geo_sep='-33.9', geo_sep_units='M', age_gps_data='', ref_station_id='0000')>


The `NMEASentence` object has different properties, depending on its sentence type.
The `GGA` message has the following properties:

    >>> msg.timestamp
    datetime.time(18, 43, 53)
    >>> msg.lat
    '1929.045'
    >>> msg.lat_dir
    'S'
    >>> msg.lon
    '02410.506'
    >>> msg.lon_dir
    'E'
    >>> msg.gps_qual
    '1'
    >>> msg.num_sats
    '04'
    >>> msg.horizontal_dil
    '2.6'
    >>> msg.altitude
    100.0
    >>> msg.altitude_units
    'M'
    >>> msg.geo_sep
    '-33.9'
    >>> msg.geo_sep_units
    'M'
    >>> msg.age_gps_data
    ''
    >>> msg.ref_station_id
    '0000'
    >>>


Additional properties besides the ones explicitly in the message data may also exist.

For example, `latitude` and `longitude` properties exist as helpers to access the geographic coordinates as python floats ([DD](http://en.wikipedia.org/wiki/Decimal_degrees), "decimal degrees") instead of the string DMS ("Degrees, minutes, seconds") format used in the NMEA protocol

    >>> msg.latitude
    -19.4840833333
    >>> msg.longitude
    24.1751


Generating
----------

You can create a `NMEASentence` object by calling the constructor with talker, message type, and data fields:

    >>> msg = pynmea2.GGA('GP', 'GGA', '184353.07', '1929.045', 'S', '02410.506', 'E', '1', '04', '2.6', '100.00', 'M', '-33.9', 'M', '', '0000')


and generate a NMEA string from a `NMEASentence` object:

    >>> str(msg)
    '$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D'


Streaming
---------

`pynmea2` can also process streams of NMEA sentences like so, by feeding chunks of data
manually:

```python
streamreader = pynmea2.NMEAStreamReader()
while 1:
    data = input.read()
    for msg in streamreader.next(data):
        print msg
```

or given a file-like device, automatically:

```python
    streamreader = pynmea2.NMEAStreamReader(input)
    while 1:
        for msg in streamreader.next():
            print msg
```

TODO
----

* Generate Sphinx docs
* Make extra NMEASentence properties writable
* Cleanup types
