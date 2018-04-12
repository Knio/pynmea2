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
        sentence_type = data[0] or data[1]
        name = manufacturer + sentence_type
        if name not in _cls.sentence_types:
            # TNLDG does not have a sentence type
            if TNLDG.match(data):
                return super(TNL, TNLDG).__new__(TNLDG)
        cls = _cls.sentence_types.get(name, _cls)
        return super(TNL, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = data[0] or data[1]
        super(TNL, self).__init__(manufacturer, data)


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
        self.subtype = 'TNL'
        super(TNLDG, self).__init(*args, **kwargs)

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
        ("Datestamp", 'datestamp', datestamp),
        ('Azimuth Angle', 'azimuth', float),
        ('AzimuthTime', 'azdt', float),
        ('Vertical Angle', 'vertical', float),
        ('VerticalTime', 'vertdt', float),
        ('Range', 'range', float),
        ('RangeTime', 'rdt', float),
        ('GPS Quality', 'gps_quality', Decimal),
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
