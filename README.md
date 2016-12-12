pynmea2
=======

`pynmea2` is a python library for the [NMEA 0183](http://en.wikipedia.org/wiki/NMEA_0183) protocol

`pynmea2` is based on [`pynmea`](https://code.google.com/p/pynmea/) by Becky Lewis

The `pynmea2` homepage is located at http://github.com/Knio/pynmea2


### Compatibility

`pynmea2` is compatable with Python 2.7 and Python 3.3

[![Build Status](https://travis-ci.org/Knio/pynmea2.png?branch=master)](https://travis-ci.org/Knio/pynmea2)
[![Coverage Status](https://coveralls.io/repos/Knio/pynmea2/badge.png?branch=master)](https://coveralls.io/r/Knio/pynmea2?branch=master)
[![Code Health](https://landscape.io/github/Knio/pynmea2/master/landscape.svg?style=flat)](https://landscape.io/github/Knio/pynmea2/master)

### Installation

The recommended way to install `pynmea2` is with
[pip](http://pypi.python.org/pypi/pip/):

    pip install pynmea2

[![PyPI version](https://badge.fury.io/py/pynmea2.png)](http://badge.fury.io/py/pynmea2)

Parsing
-------

You can parse individual NMEA sentences using the `parse(data, check=False)` function, which takes a string containing a
NMEA 0183 sentence and returns a `NMEASentence` object. Note that the leading '$' is optional and trailing whitespace is ignored when parsing a sentence.

With `check=False`, `parse` will accept NMEA messages that do not have checksums, however it will still raise `pynmea2.ChecksumError` if they are present. `check=True` will also raise `ChecksumError` if the checksum is missing.

Example:

```python
>>> import pynmea2
>>> msg = pynmea2.parse("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D")
>>> msg
<GGA(timestamp=datetime.time(18, 43, 53), lat='1929.045', lat_dir='S', lon='02410.506', lon_dir='E', gps_qual='1', num_sats='04', horizontal_dil='2.6', altitude=100.0, altitude_units='M', geo_sep='-33.9', geo_sep_units='M', age_gps_data='', ref_station_id='0000')>
```

The `NMEASentence` object has different properties, depending on its sentence type.
The `GGA` message has the following properties:

```python
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
```

Additional properties besides the ones explicitly in the message data may also exist.

For example, `latitude` and `longitude` properties exist as helpers to access the geographic coordinates as python floats ([DD](http://en.wikipedia.org/wiki/Decimal_degrees), "decimal degrees") instead of the DDDMM.MMMM ("Degrees, minutes, seconds") format used in the NMEA protocol. `latitude_minutes`, `latitude_seconds`, `longitude_minutes`, and `longitude_seconds` are also supported and allow easy creation of differently formatted location strings.

```python
>>> msg.latitude
-19.4840833333
>>> msg.longitude
24.1751
>>> '%02d°%07.4f′' % (msg.latitude, msg.latitude_minutes)
'-19°29.0450′'
>>> '%02d°%02d′%07.4f″' % (msg.latitude, msg.latitude_minutes, msg.latitude_seconds)
"-19°29′02.7000″"
```

Generating
----------

You can create a `NMEASentence` object by calling the constructor with talker, message type, and data fields:

```python
>>> msg = pynmea2.GGA('GP', 'GGA', ('184353.07', '1929.045', 'S', '02410.506', 'E', '1', '04', '2.6', '100.00', 'M', '-33.9', 'M', '', '0000'))
```


and generate a NMEA string from a `NMEASentence` object:

```python
>>> str(msg)
'$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D'
```

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


If your stream is noisy and contains errors, you can set some basic error handling with the [`errors` parameter of the `NMEAStreamReader` constructor.](pynmea2/stream.py#L12)
