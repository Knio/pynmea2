# Magellan

from decimal import Decimal

from ... import nmea
from ... import nmea_utils


class MGN(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[0]
        cls = _cls.sentence_types.get(name, _cls)
        return super(MGN, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = manufacturer + data[0]
        super(MGN, self).__init__(manufacturer, data)


class MGNWPL(MGN, nmea_utils.LatLonFix):
    """ Magellan Waypoint Location

    https://github.com/wb2osz/direwolf/blob/master/waypoint.c

    $PMGNWPL,ddmm.mmmm,ns,dddmm.mmmm,ew,alt,unit,wname,comment,icon,xx*99
    Where,
        ddmm.mmmm,ns    is latitude
        dddmm.mmmm,ew   is longitude
        alt             is altitude
        unit            is M for meters or F for feet
        wname           is the waypoint name
        comment         is message or comment
        icon            is one or two letters for icon code
        xx              is waypoint type which is optional, not well
                        defined, and not used in their example.
        *99             is checksum
    """
    fields = (
        ("Subtype", "subtype"),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Altitude", "altitude", Decimal),
        ("Altitude Units (Feet/Meters)", "altitude_unit"),
        ("Waypoint Name", "wname"),
        ("Comment", "comment"),
        ("Icon", "icon"),
        ("Waypoint Type", "type")
    )
