'''
Support for proprietary messages from Furuno receivers.
'''
# Implemented by Joep de Jong
# pylint: disable=wildcard-import,unused-wildcard-import

from ... import nmea
from ...nmea_utils import *

class FEC(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[1]
        cls = _cls.sentence_types.get(name, _cls)
        return super(FEC, cls).__new__(cls)

class FECGPatt(FEC):
    """
        Furuno GPatt Message

        $PFEC,GPatt,aaa.a,bb.b,cc.c,*hh<CR><LF>
        $PFEC: Talker identifier + sentence formatter*
        GPatt: Global positioning attitude, sentence formatter
        aaa.a: Yaw (degrees)*
        bb.b: Pitch (degrees)*
        cc.c: Roll (degrees)*
        *hh: Checksum*
    """
    fields = (
        ('R', '_r'),
        ('Subtype', 'subtype'),
        ('Yaw', 'yaw', float),
        ('Pitch', 'pitch', float),
        ('Roll', 'roll', float),
    )


class FECGPhve(FEC):
    """
        Furuno GPatt Message

        $PFEC,GPhve,xx.xxx,A*hh<CR><LF>
        $PFEC: Talker identifier
        GPhve: Datagram identifier
        xx.xxx: Heave (Metres)
        A: Status
        *hh: Checksum
    """

    fields = (
        ("R", "_r"),
        ("Subtype", "subtype"),
        ("Heave", "heave", float),
    )
