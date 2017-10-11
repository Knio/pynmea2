""" Support for proprietary message(s) from RD Instruments
"""

from ... import nmea

class RDI(nmea.ProprietarySentence):
    """ RD Instruments message. Only one sentence known?
    """
    sentence_types = {}
    def __new__(_cls, *_):
        return super(RDI, RDID).__new__(RDID)

class RDID(RDI):
    """ RD Instruments heading, pitch and roll data
    """
    def __init__(self, manufacturer, data):
        self.sentence_type = 'D'
        # pylint: disable=bad-super-call
        super(RDI, self).__init__(manufacturer, data[1:])

    fields = (
        ("Pitch", "pitch", float),
        ("Roll", "roll", float),
        ("Heading", "heading", float)
    )
