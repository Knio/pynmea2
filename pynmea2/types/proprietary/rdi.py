'''
Support for proprietary message(s) from RD Instruments
'''

from ... import nmea


class RDI(nmea.ProprietarySentence):
    '''
    RD Instruments message. Only one sentence known?
    '''
    sentence_types = {}
    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[0]
        cls = _cls.sentence_types.get(name, _cls)
        return super(RDI, cls).__new__(cls)


class RDID(RDI):
    '''
    RD Instruments heading, pitch and roll data
    '''
    fields = (
        ('Subtype', 'subtype'),
        ("Pitch", "pitch", float),
        ("Roll", "roll", float),
        ("Heading", "heading", float)
    )
