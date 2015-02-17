# SiRF

from ... import nmea


class SRF(nmea.ProprietarySentence):
    sentence_types = {}
    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[0]
        cls = _cls.sentence_types.get(name, _cls)
        return super(SRF, cls).__new__(cls)


class SRF103(SRF):
    fields = (
        ('Sentence type', 'sentence'),
        # 00=GGA
        # 01=GLL
        # 02=GSA
        # 03=GSV
        # 04=RMC
        # 05=VTG
        ('Command', 'command'),
        # 0=Set
        # 1=Query
        ('Rate', 'rate'),
        ('Checksum', 'checksum'),
        # 0=No, 1=Yes
    )


class SRF100(SRF):
    fields = (
        ('Protocol', 'protocol'),
        # 0 = SiRF Binary
        # 1 = NMEA
        ('Baud Rate', 'baud'),
        # 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200
        ('Data bits', 'databits'),
        # 8 (, 7 in NMEA)
        ('Stop bits', 'stopbits'),
        # 0, 1
        ('Parity', 'parity'),
        # 0, 1=Odd, 2=Even
    )
