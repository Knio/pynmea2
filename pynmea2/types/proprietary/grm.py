# Garmin

from decimal import Decimal

from ... import nmea

class GRM(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[0]
        cls = _cls.sentence_types.get(name, _cls)
        return super(GRM, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = manufacturer + data[0]
        super(GRM, self).__init__(manufacturer, data)


class GRME(GRM):
    """ GARMIN Estimated position error
    """
    fields = (
        ("Subtype", "subtype"),
        ("Estimated Horiz. Position Error", "hpe", Decimal),
        ("Estimated Horiz. Position Error Unit (M)", "hpe_unit"),
        ("Estimated Vert. Position Error", "vpe", Decimal),
        ("Estimated Vert. Position Error Unit (M)", "vpe_unit"),
        ("Estimated Horiz. Position Error", "osepe", Decimal),
        ("Overall Spherical Equiv. Position Error", "osepe_unit"),
    )


class GRMM(GRM):
    """ GARMIN Map Datum
    """
    fields = (
        ("Subtype", "subtype"),
        ('Currently Active Datum', 'datum'),
    )


class GRMW(GRM):
    """ GARMIN Waypoint Information

    https://www8.garmin.com/support/pdf/NMEA_0183.pdf
    https://github.com/wb2osz/direwolf/blob/master/waypoint.c

    $PGRMW,wname,alt,symbol,comment*99
    Where,
       wname		is waypoint name.  Must match existing waypoint.
       alt		is altitude in meters.
       symbol		is symbol code.  Hexadecimal up to FFFF.
                    See Garmin Device Interface Specification
                    001-0063-00 for values of "symbol_type."
       comment      is comment for the waypoint.
       *99		    is checksum
    """
    fields = (
        ("Subtype", "subtype"),
        ("Waypoint Name", "wname"),
        ("Altitude", "altitude", Decimal),
        ("Symbol", "symbol"),
        ("Comment", "comment"),
    )


class GRMZ(GRM):
    """ GARMIN Altitude Information
    """
    fields = (
        ("Subtype", "subtype"),
        ("Altitude", "altitude", Decimal),
        ("Altitude Units (Feet)", "altitude_unit"),
        ("Positional Fix Dimension (2=user, 3=GPS)", "pos_fix_dim"),
    )
