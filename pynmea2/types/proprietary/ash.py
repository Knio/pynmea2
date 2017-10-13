'''
Support for proprietary messages from Ashtech receivers.
'''
# pylint: disable=wildcard-import,unused-wildcard-import
from decimal import Decimal
import re

from ... import nmea
from ...nmea_utils import *


class ASH(nmea.ProprietarySentence):
    '''
    Generic Ashtech Response Message
    '''
    sentence_types = {}
    def __new__(_cls, manufacturer, data):
        '''
        Return the correct sentence type based on the first field
        '''
        sentence_type = data[1]
        name = manufacturer + 'R' + sentence_type
        if name not in _cls.sentence_types:
            # ASHRATT does not have a sentence type
            if ASHRATT.match(data):
                return super(ASH, ASHRATT).__new__(ASHRATT)
        cls = _cls.sentence_types.get(name, ASH)
        return super(ASH, cls).__new__(cls)


class ASHRATT(ASH):
    '''
    RT300 proprietary attitude sentence
    '''
    @staticmethod
    def match(data):
        return re.match(r'^\d{6}\.\d{3}$', data[1])

    def __init__(self, *args, **kwargs):
        self.subtype = 'ATT'
        super(ASHRATT, self).__init__(*args, **kwargs)

    fields = (
        ('R', '_r'),
        ('Timestamp', 'timestamp', timestamp),
        ('Heading Angle', 'true_heading', float),
        ('Is True Heading', 'is_true_heading'),
        ('Roll Angle', 'roll', float),
        ('Pitch Angle', 'pitch', float),
        ('Heave', 'heading', float),
        ('Roll Accuracy Estimate', 'roll_accuracy', float),
        ('Pitch Accuracy Estimate', 'pitch_accuracy', float),
        ('Heading Accuracy Estimate', 'heading_accuracy', float),
        ('Aiding Status', 'aiding_status', Decimal),
        ('IMU Status', 'imu_status', Decimal),
    )


class ASHRHPR(ASH):
    '''
    Ashtech HPR Message
    '''
    fields = (
        ('R', '_r'),
        ('Subtype', 'subtype'),
        ('Timestamp', 'timestamp', timestamp),
        ('Heading Angle', 'heading', Decimal),
        ('Pitch Angle', 'pitch', Decimal),
        ('Roll Angle', 'roll', Decimal),
        ('Carrier measurement RMS', 'carrier_rms', Decimal),
        ('Baseline measurement RMS', 'baseline_rms', Decimal),
        ('Integer Ambiguity', 'integer_ambiguity'),
        ('Mode', 'mode'),
        ('Status', 'status'),
        ('PDOP', 'pdop', float),
    )


class ASHRLTN(ASH):
    '''
    Ashtech LTN Message
    '''
    fields = (
        ('R', '_r'),
        ('Subtype', 'subtype'),
        ('Latency (ms)', 'latency', int),
    )


class ASHRPOS(ASH, LatLonFix):
    '''
    Ashtech POS Message
    '''
    fields = (
        ('R', '_r'),
        ('Subtype', 'subtype'),
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
    '''
    Ashtech VEL Message
    '''
    fields = (
        ('R', '_r'),
        ('Subtype', 'subtype'),
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
