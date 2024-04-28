# -- TRIMBLE -- #

# pylint: disable=wildcard-import,unused-wildcard-import
from decimal import Decimal
from ... import nmea
from ...nmea_utils import *
""" Support for proprietary messages from BD9xx recievers.
    Documentation: www.trimble.com/OEM_ReceiverHelp/v4.85/en/
"""

class TNL(nmea.ProprietarySentence):
    sentence_types = {}
    """
        Generic Trimble Message
    """
    def __new__(_cls, manufacturer, data):
        '''
            Return the correct sentence type based on the first field
        '''
        sentence_type = data[1]
        name = manufacturer + sentence_type
        if name not in _cls.sentence_types:
            # TNLDG does not have a sentence type
            if TNLDG.match(data):
                return super(TNL, TNLDG).__new__(TNLDG)
        cls = _cls.sentence_types.get(name, TNL)
        return super(TNL, cls).__new__(cls)


class TNLAVR(TNL):
    """
        Trimble AVR Message
    """
    fields = (
        ('Empty', '_'),
        ('Sentence Type', 'type'),
        ('Timestamp', 'timestamp', timestamp),
        ('Yaw Angle', 'yaw_angle'),
        ('Yaw', 'yaw'),
        ('Tilt Angle', 'tilt_angle'),
        ('Tilt', 'tilt'),
        ('Roll Angle', 'roll_angle'),
        ('Roll', 'roll'),
        ('Baseline Range', 'baseline'),
        ('GPS Quality', 'gps_quality'),
        ('PDOP', 'pdop'),
        ('Total number of satelites in use', 'num_sats'),
    )


class TNLBPQ(TNL, LatLonFix, DatetimeFix):
    """
        Trimble BPQ Message
    """
    fields = (
        ('Empty', '_'),
        ('Sentence Type', 'type'),
        ('Timestamp', 'timestamp', timestamp),
        ("Datestamp", "datestamp", datestamp),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ('Height Ellipsoid', 'height'),
        ('Meters', 'meters'),
        ('Mode fix type', 'mode_fix_type'),
        ('Total number of satelites in use', 'num_sats'),
    )

class TNLDG(TNL):
    """
        Trimble DG message (L-band, beacon signal strength, etc)
    """
    @staticmethod
    def match(data):
        return re.match(r'\d+\.\d{1}', data[1])

    def __init__(self, *args, **kwargs):
        self.subtype = 'DG'
        super(TNLDG, self).__init__(*args, **kwargs)

    fields = (
        ('Empty', '_'),
        ('Signal strength', 'strength', float),
        ('SNR in db', 'snr', float),
        ('Signal frequency in kHz', 'frequency', float),
        ('Bit rate', 'bitrate', Decimal),
        ('Channel number', 'channel_no', Decimal),
        ('Tracking status', 'status'),
        ('Channel used', 'channel_used'),
        ('Tracking performance indicator', 'performance', Decimal),
    )

class TNLGGK(TNL, LatLonFix, DatetimeFix):
    """
        Trimble GGK Message
    """
    fields = (
        ('Empty', '_'),
        ('Sentence Type', 'type'),
        ('Timestamp', 'timestamp', timestamp),
        ("Datestamp", "datestamp", datestamp),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ('GPS Quality', 'quality'),
        ('Total number of satelites in use', 'num_sats'),
        ('DOP', 'dop'),
        ('Height Ellipsoid', 'height'),
        ('Meters', 'meters'),
        ('Mode fix type', 'mode_fix_type'),
    )


class TNLVGK(TNL, DatetimeFix):
    """
        Trimble VGK (vector information) message
    """
    fields = (
        ('Empty', '_'),
        ('Sentence Type', 'type'),
        ('Timestamp', 'timestamp', timestamp),
        ('Datestamp', 'datestamp', datestamp),
        ('East component', 'east', float),
        ('North component', 'north', float),
        ('Up component', 'up', float),
        ('GPS Quality', 'gps_quality'),
        ('Number of satelites', 'num_sats', Decimal),
        ('DOP of fix', 'dop', float),
        ('Meters', 'meters'),
    )

class TNLVHD(TNL, DatetimeFix):
    """
        Trimble VHD Message
    """
    fields = (
        ('Empty', '_'),
        ('Sentence Type', 'type'),
        ('Timestamp', 'timestamp', timestamp),
        ('Datestamp', 'datestamp', datestamp),
        ('Azimuth Angle', 'azimuth', float),
        ('AzimuthTime', 'azdt', float),
        ('Vertical Angle', 'vertical', float),
        ('VerticalTime', 'vertdt', float),
        ('Range', 'range', float),
        ('RangeTime', 'rdt', float),
        ('GPS Quality', 'gps_quality'),
        ('Total number of satelites in use', 'num_sats', Decimal),
        ('PDOP', 'pdop', float),
    )

class TNLPJK(TNL, DatetimeFix):
    """
        Trimble PJK message
    """
    fields = (
        ('Empty', '_'),
        ('Sentence Type', 'type'),
        ('Timestamp', 'timestamp', timestamp),
        ('Datestamp', 'datestamp', datestamp),
        ('Northing', 'northing', float),
        ('North', 'north'),
        ('Easting', 'easting', float),
        ('East', 'east'),
        ('GPS Quality', 'gps_quality'),
        ('Number of satellites', 'num_sats', Decimal),
        ('DOP of fix', 'dop', float),
        ('Height of antenna phase center', 'height'),
        ('Meters', 'meters'),
    )

class TNLPJT(TNL):
    """
        Trimble PJT Message
    """
    fields = (
        ('Empty', '_'),
        ('Sentence Type', 'type'),
        ('Coordinate System', 'coord_name'),
        ('Project Name', 'project_name'),
    )

class TNLEVT(TNL, DatetimeFix):
    """
        Trimble EVT message (used for events like hardware triggers)

        0 	Talker ID $PTNL
        1 	Message ID EVT
        2 	Event time. UTC time of event in format hhmmss.ssssss
        3 	Port number. Port event markers receiver: "1" or "2" (optional),
                if two ports are available.
        4 	NNNNNN. Incremental number of events on each independent port.
        5 	WWWW. Week number of event (since 06 January 1980).
        6 	Day of week. Days denoted 0 = Sunday…6 = Saturday.
        7 	Leap second. UTC Leap Second offset from GPS time,
        8 	The checksum data, always begins with *

        Example message:
        $PTNL,EVT,131007.999785,2,460,2181,5,18*72
    """
    fields = (
        ('Empty', '_'),
        ('Sentence Type', 'type'),
        ('Timestamp', 'timestamp', timestamp),
        ('Port Number', 'port_num', int),
        ('Event Number', 'event_num', int),
        ('GPS Week Number', 'gps_week_num', int),
        ('GPS Day of the Week', 'gps_day_num', int),
        ('Leap Seconds', 'leap_secs', int)
    )
