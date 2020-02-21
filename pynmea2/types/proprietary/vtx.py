# Vectronix Moskito TI (LRF)

from decimal import Decimal

from ... import nmea
from ...nmea_utils import *

class VTX(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[1]
        cls = _cls.sentence_types.get(name, _cls)
        return super(VTX, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = manufacturer + data[0]
        super(VTX, self).__init__(manufacturer, data)


class VTX0002(VTX):
    """ Vectronix measurement: laser distance and angles (degrees) with declination
    """
    fields = (
        ("Message Placeholder", "mplaceholder"),
        ("Subtype", "subtype"),
        ("Measurement ID", "measurement_id", int),
        ("Distance (meters)", "dist", float),
        ("Distance unit", "dist_unit"),
        ("Direction (degrees)", "direction", float),
        ("Direction unit", "direction_unit"),
        ("Vertical angle (degrees)", "va", float),
        ("Magnetic declination (degrees)", "decl", float),
        ("Magnetic declination ref (E/W)", "decl_ref")
    )


class VTX0000(VTX):
    """ Vectronix raw measurement: laser distance and angles (radians) without declination
    """
    fields = (
        ("Message Placeholder", "mplaceholder"),
        ("Subtype", "subtype"),
        ("Distance (meters)", "dist", float),
        ("Distance unit", "dist_unit"),
        ("Direction (radians)", "direction", float),
        ("Roll angle (radians)", "roll", float),
        ("Vertical angle (radians)", "va", float),
        ("Angular units type", "angle_units")
    )


class VTX0020(VTX, LatLonFix):
    """ Vectronix self location: lat, long, altitude
    """
    fields = (
        ("Message Placeholder", "mplaceholder"),
        ("Subtype", "subtype"),
        ("Measurement ID", "measurement_id", int),
        ('Latitude', 'lat'),
        ('Latitude Direction', 'lat_dir'),
        ('Longitude', 'lon'),
        ('Longitude Direction', 'lon_dir'),
        ('Altitude above WGS84 ellipsoid, meters', 'altitude', float),
        ('Altitude units', 'altitude_units')
    )


class VTX0012(VTX, LatLonFix):
    """ Vectronix target location: lat, long, altitude, gain
    """
    fields = (
        ("Message Placeholder", "mplaceholder"),
        ("Subtype", "subtype"),
        ("Measurement ID", "measurement_id", int),
        ('Latitude', 'lat'),
        ('Latitude Direction', 'lat_dir'),
        ('Longitude', 'lon'),
        ('Longitude Direction', 'lon_dir'),
        ('Altitude above WGS84 ellipsoid, meters', 'altitude', float),
        ('Altitude units', 'altitude_units'),
        ('Gain (meters)', 'gain', float),
        ('Gain units', 'gain_units')
    )
