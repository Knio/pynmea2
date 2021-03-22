# pylint: disable=wildcard-import,unused-wildcard-import
from decimal import Decimal

from ... import nmea
from ...nmea_utils import *


# u-blox
class UBX(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[1]
        cls = _cls.sentence_types.get(name, _cls)
        return super(UBX, cls).__new__(cls)


class UBX00(UBX, LatLonFix):
    """ Lat/Long Position Data
    """
    fields = (
        ("Blank", "_blank"),
        ("UBX Type", "ubx_type"),
        ("Timestamp (UTC)", "timestamp", timestamp),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Altitude above user datum ellipsoid", "alt_ref"),
        ("Navigation Status", "nav_stat"),
        ("Horizontal Accuracy Estimate", "h_acc"),
        ("Vertical Accuracy Estimate", "v_acc"),
        ("Speed over Ground", "sog"),
        ("Course over Ground", "cog"),
        ("Vertical Velocity", "v_vel"),
        ("Age of Differential Corrections", "diff_age"),
        ("Horizontal Dilution of Precision", "hdop"),
        ("Vertical Dilution of Precision", "vdop"),
        ("Time Dilution of Precision", "tdop"),
        ("Number of Satellites Used", "num_svs"),
        ("Reserved", "reserved")
    )


class UBX03(UBX):
    """ Satellite Status
    """
    fields = (
        ("Blank", "_blank"),
        ("UBX Type", "ubx_type"),
        ("Number of GNSS Satellites Tracked", "num_sv", int),
    )

    @property
    def satellite_list(self):
        return self.data[1:]


class UBX04(UBX):
    """ Time and Day Clock Information
    """
    fields = (
        ("Blank", "_blank"),
        ("UBX Type", "ubx_type"),
        ("UTC Time", "time", timestamp),
        ("UTC Date", "date", datestamp),
        ("UTC Time of Week", "utc_tow"),
        ("UTC Week Number", "utc_wk"),
        ("Leap Seconds", "leap_sec"),
        ("Receiver Clock Bias", "clk_bias", int),
        ("Receiver Clock Drift", "clk_drift", Decimal),
        ("Time Pulse Granularity", "tp_gran", int),
    )
