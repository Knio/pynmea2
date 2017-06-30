# -- ASHTECH -- #
from decimal import Decimal
# pylint: disable=wildcard-import,unused-wildcard-import
from ... import nmea
from ...nmea_utils import *
""" Support for proprietary messages from Ashtech receivers.
    Documentation: www.trimble.com/OEM_ReceiverHelp/v4.85/en/
"""

class ASH(nmea.ProprietarySentence):
    sentence_types = {}
    """
        Generic Ashtech Response Message
    """
    def __new__(_cls, manufacturer, data):
        '''
            Return the correct sentence type based on the first field
        '''
        sentence_type = data[1]
        name = manufacturer + 'R' + sentence_type
        cls = _cls.sentence_types.get(name, _cls)
        return super(ASH, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = data[1]
        super(ASH, self).__init__(manufacturer, data[2:])

class ASHRHPR(ASH):
    """
        Ashtech HPR Message
    """
    fields = (
        ('Timestamp', 'timestamp', timestamp),
        ('Heading Angle', 'heading', Decimal),
        ('Pitch Angle', 'pitch', Decimal),
        ('Roll Angle', 'roll', Decimal),
        ('Carrier measurement RMS', 'carrier_rms', Decimal),
        ('Baseline measurement RMS', 'baseline_rms', Decimal),
        ('Integer Ambiguity', 'integer_ambiguity'),
        ('Mode', 'mode'),
        ('Status', 'status'),
        ('PDOP', 'pdop',float),
    )

class ASHRLTN(ASH):
    """
        Ashtech LTN Message
    """
    fields = (
        ('Latency (ms)', 'latency', int),
    )

class ASHRPOS(ASH,LatLonFix):
    """
        Ashtech POS Message
    """
    fields = (
        ('Solution Type', 'mode', int),
        ('Satellites used in Solution', 'sat_count', int),
        ('Timestamp', 'timestamp', timestamp),
        ('Latitude', 'lat'),
        ('Latitude Direction', 'lat_dir'),
        ('Longitude', 'lon'),
        ('Longitude Direction', 'lon_dir'),
        ('Altitude above WGS84 ellipsoid, meters', 'altitude'),
        ('Empty', '__'),
        ("True Track/Course Over Ground", "course", float),
        ("Speed Over Ground", "spd_over_grnd", float),
        ('Vertical Velocity', 'vertical_velocity', Decimal),
        ('PDOP', 'pdop', float),
        ('HDOP', 'hdop', float),
        ('VDOP', 'vdop', float),
        ('TDOP', 'tdop', float),
        ('Base station ID', 'station_id', int)
    )

class ASHRVEL(ASH):
    """
        Ashtech VEL Message
    """
    fields = (
        ('ENU', 'enu', int),
        ('Timestamp', 'timestamp', timestamp),
        ('Easting', 'easting', Decimal),
        ('Northing', 'northing', Decimal),
        ('Vertical Velocity', 'vertical', Decimal),
        ('Easting RMS', 'easting_rms', Decimal),
        ('Northing RMS', 'northing_rms', Decimal),
        ('Vertical RMS', 'vertical_rms', Decimal),
        ('Applied effective velocity smoothing interval (ms)', 'smoothing', Decimal),
    )
