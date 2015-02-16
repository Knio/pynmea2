# Garmin

from ... import nmea

class GRM(nmea.ProprietarySentence):
    sentence_types = {}
    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[0]
        cls = _cls.sentence_types.get(name, _cls)
        return super(GRM, cls).__new__(cls)


class GRME(GRM):
    """ GARMIN Estimated position error
    """
    fields = (
        ("Estimated Horiz. Position Error", "hpe"),
        ("Estimated Horiz. Position Error Unit (M)", "hpe_unit"),
        ("Estimated Vert. Position Error", "vpe"),
        ("Estimated Vert. Position Error Unit (M)", "vpe_unit"),
        ("Estimated Horiz. Position Error", "osepe"),
        ("Overall Spherical Equiv. Position Error", "osepe_unit")
    )


class GRMM(GRM):
    """ GARMIN Map Datum
    """
    fields = (
        ('Currently Active Datum', 'datum'),
    )


class GRMZ(GRM):
    """ GARMIN Altitude Information
    """
    fields = (
        ("Altitude", "altitude"),
        ("Altitude Units (Feet)", "altitude_unit"),
        ("Positional Fix Dimension (2=user, 3=GPS)", "pos_fix_dim")
    )



