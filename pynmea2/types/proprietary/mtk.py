# -- TRIMBLE -- #

# pylint: disable=wildcard-import,unused-wildcard-import
from ... import nmea
from ...nmea_utils import *
""" Support for proprietary messages from MediaTek recievers.
    Documentation: https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf
"""


class MTK(nmea.ProprietarySentence):
    sentence_types = {}
    """
        Generic MTK Message
    """
    def __new__(_cls, manufacturer, data):
        '''
            Return the correct sentence type based on the first field
        '''
        sentence_type = data[0] or data[1]
        name = manufacturer + sentence_type
        cls = _cls.sentence_types.get(name, _cls)
        return super(MTK, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = data[0] or data[1]
        super(MTK, self).__init__(manufacturer, data)


class MTK001(MTK):
    """
        001 MTK_ACK
    """
    fields = (
        ('Blank', '_'),
        ('Cmd', 'cmd', int),
        ('Flag', 'flag', int),
    )


class MTK010(MTK):
    """
        010 MTK_SYS_MSG
    """
    fields = (
        ('Blank', '_'),
        ('Data', 'data', int),  # 0 = UNKNOWN
                                # 1 = STARTUP
                                # 2 = Notification for host aiding EPO
                                # 3 = Notification for transition to Normal mode success
    )


class MTK011(MTK):
    """
        011 MTK_TXT_MSG
    """
    fields = (
        ('Blank', '_'),
        ('Text', 'text'),
    )


class MTK101(MTK):
    """
        101 MTK_CMD_HOT_START
    """
    fields = (
        ('Blank', '_'),
    )


class MTK102(MTK):
    """
        102 MTK_CMD_WARM_START
    """
    fields = ( 
        ('Blank', '_'),
    )


class MTK103(MTK):
    """
        103 MTK_CMD_COLD_START
    """
    fields = (
        ('Blank', '_'),
    )


class MTK104(MTK):
    """
        104 MTK_CMD_FULL_COLD_START
    """
    fields = (
        ('Blank', '_'),
    )


class MTK220(MTK):
    """
        220 MTK_SET_NMEA_UPDATERATE
    """
    fields = (
        ('Blank', '_'),
        ("FixInterval", "fix_interval", int),  # Fix interval in milliseconds from 100 to 10,000
    )
