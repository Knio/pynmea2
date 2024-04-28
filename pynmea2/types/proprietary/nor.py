'''
Support for proprietary messages from Nortek Doppler Velocity Log (DVL).
'''

from ... import ProprietarySentence, nmea_utils
from datetime import datetime

class NOR(ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[0]
        cls = _cls.sentence_types.get(name, _cls)
        return super(NOR, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = manufacturer + data[0]
        super(NOR, self).__init__(manufacturer, data[1:])

    def identifier(self):
        return 'P%s,' % (self.sentence_type)

##################################################################
##                                                              ##
## DVL Bottom Track ASCII formats                               ##
##                                                              ##
## Invalid estimates of Velocity are set to set to -32.768.     ##
## Invalid estimates of Range are set to 0.0.                   ##
## Invalid estimates of FOM are set to 10.0                     ##
##################################################################

class NORBT0(NOR, nmea_utils.DatetimeFix):
    # Bottom Track DF350/DF351 - NMEA $PNORBT1/$PNORBT0
    # Example: $PNORBT0,1,040721,131335.3341,23.961,-48.122,-32.76800,10.00000,0.00,0x00000000*48

    fields = (
        ('Beam number', 'beam', int),
        ('Date', 'datestamp', nmea_utils.datestamp),
        ('Time', 'timestamp', nmea_utils.timestamp),
        ('Time (Trigger)', 'dt1', float),
        ('Time (NMEA)', 'dt2', float),
        ('Beam Velocity', 'bv', float),
        ('Figure of Merit', 'fom', float),
        ('Vertical Distance', 'dist', float),
        ('Status ', 'stat'),
    )

class NORBT4(NOR, nmea_utils.DatetimeFix):
    # Bottom Track DF354/DF355 - NMEA $PNORBT3/$PNORBT4
    # Example: $PNORBT4,1.234,-1.234,1.234,23.4,12.34567,12.3*09

    fields = (
        ('Time (Trigger)', 'dt1', float),
        ('Time (NMEA)', 'dt2', float),
        ('Speed of Sound', 'sound_speed', float),
        ('Direction', 'dir', float),
        ('Figure of Merit', 'fom', float),
        ('Vertical Distance', 'dist', float),
    )

class NORBT7(NOR):
    # Bottom Track DF356/DF357 - NMEA $PNORBT6/$PNORBT7
    # Example: $PNORBT7,1452244916.7508,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45*39

    fields = (
        ('Ping Time', 'timestamp', lambda x: datetime.utcfromtimestamp(float(x))),
        ('Time (Trigger)', 'dt1', float),
        ('Time (NMEA)', 'dt2', float),
        ('Velocity X', 'vx', float),
        ('Velocity Y', 'vy', float),
        ('Velocity Z', 'vz', float),
        ('Figure of Merit', 'fom', float),
        ('Vertical Distance Beam 1', 'd1', float),
        ('Vertical Distance Beam 2', 'd2', float),
        ('Vertical Distance Beam 3', 'd3', float),
        ('Vertical Distance Beam 4', 'd4', float),
    )

class NORBT9(NOR):
    # Bottom Track DF358/DF359 - NMEA $PNORBT8/$PNORBT9
    # Example: $PNORBT9,1452244916.7508,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45,23.4,1567.8,1.2,12.3,0x000FFFFF*1E

    fields = (
        ('Ping Time', 'timestamp', lambda x: datetime.utcfromtimestamp(float(x))),
        ('Time (Trigger)', 'dt1', float),
        ('Time (NMEA)', 'dt2', float),
        ('Velocity X', 'vx', float),
        ('Velocity Y', 'vy', float),
        ('Velocity Z', 'vz', float),
        ('Figure of Merit', 'fom', float),
        ('Vertical Distance Beam 1', 'd1', float),
        ('Vertical Distance Beam 2', 'd2', float),
        ('Vertical Distance Beam 3', 'd3', float),
        ('Vertical Distance Beam 4', 'd4', float),
        ('Battery Voltage', 'battery_voltage', float),
        ('Speed of Sound', 'sound_speed', float),
        ('Pressure', 'pressure', float),
        ('Temperature', 'temp', float),
        ('Status ', 'stat'),
    )

##################################################################
##                                                              ##
## DVL Water Track ASCII formats                                ##
##                                                              ##
## Invalid estimates of Velocity are set to set to -32.768.     ##
## Invalid estimates of Range are set to 0.0.                   ##
## Invalid estimates of FOM are set to 10.0                     ##
##################################################################

class NORWT4(NOR):
    # Water Track DF404/DF405 - NMEA $PNORWT3/$PNORWT4
    # Example: $PNORWT4,1.2345,-1.2345,1.234,23.4,12.34,12.3*1C

    fields = (
        ('Time Trigger ', 'dt1', float),
        ('Time NMEA', 'dt2', float),
        ('Speed of sound', 'sound_speed', float),
        ('Direction', 'dir', float),
        ('Figure of Merit', 'fom', float),
        ('Vertical Distance', 'dist', float),
    )

class NORWT7(NOR):
    # Water Track DF406/DF407 - NMEA $PNORWT6/$PNORWT7
    # Example: $PNORWT7,1452244916.7508,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45*2C

    fields = (
        ('Ping Time', 'timestamp', lambda x: datetime.utcfromtimestamp(float(x))),
        ('Time (Trigger)', 'dt1', float),
        ('Time (NMEA)', 'dt2', float),
        ('Velocity X', 'vx', float),
        ('Velocity Y', 'vy', float),
        ('Velocity Z', 'vz', float),
        ('Figure of Merit', 'fom', float),
        ('Vertical Distance Beam 1', 'd1', float),
        ('Vertical Distance Beam 2', 'd2', float),
        ('Vertical Distance Beam 3', 'd3', float),
        ('Vertical Distance Beam 4', 'd4', float),
    )

class NORWT9(NOR):
    # Water Track DF408/DF409 - NMEA $PNORWT8/$PNORWT9
    # Example: $PNORWT9,1452244916.7508,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45,23.4,1567.8,1.2,12.3,0x000FFFFF*0B

    fields = (
        ('Ping Time', 'timestamp', lambda x: datetime.utcfromtimestamp(float(x))),
        ('Time (Trigger)', 'dt1', float),
        ('Time (NMEA)', 'dt2', float),
        ('Velocity X', 'vx', float),
        ('Velocity Y', 'vy', float),
        ('Velocity Z', 'vz', float),
        ('Figure of Merit', 'fom', float),
        ('Vertical Distance Beam 1', 'd1', float),
        ('Vertical Distance Beam 2', 'd2', float),
        ('Vertical Distance Beam 3', 'd3', float),
        ('Vertical Distance Beam 4', 'd4', float),
        ('Battery Voltage', 'battery_voltage', float),
        ('Speed of Sound', 'sound_speed', float),
        ('Pressure', 'pressure', float),
        ('Temperature', 'temp', float),
        ('Status ', 'stat'),
    )

##################################################################
##                                                              ##
## DVL Current Profile ASCII formats                            ##
##                                                              ##
##################################################################

class NORI1(NOR):
    # Information Data DF101/DF102 - NMEA Format 1 and 2
    # Example: $PNORI1,4,123456,3,30,1.00,5.00,BEAM*5B

    fields = (
        ('Instrument type', 'it', int),
        ('Head ID', 'sn', int),
        ('Number of Beams', 'nb', int),
        ('Number of Cells', 'nc', int),
        ('Blanking Distance', 'bd', float),
        ('Cell Size', 'cs', float),
        ('Coordinate System', 'cy', str),
    )

class NORS1(NOR, nmea_utils.DatetimeFix):
    # Sensors Data DF101/DF102 - NMEA Format 1 and 2
    # Example: $PNORS1,161109,132455,0,34000034,23.9,1500.0,123.4,0.02,45.6,0.02,23.4,0.02,123.456,0.02,24.56*51

    fields = (
        ('Date', 'datestamp', nmea_utils.datestamp),
        ('Time', 'timestamp', nmea_utils.timestamp),
        ('Error Code', 'ec', int),
        ('Status Code', 'sc'),
        ('Battery Voltage', 'battery_voltage', float),
        ('Speed of Sound', 'sound_speed', float),
        ('Heading', 'heading', float),
        ('Heading Std. Dev.', 'heading_std', float),
        ('Pitch', 'pitch', float),
        ('Pitch Std. Dev.', 'pitch_std', float),
        ('Roll', 'roll', float),
        ('Roll Std. Dev.', 'roll_std', float),
        ('Pressure', 'pressure', float),
        ('Pressure Std. Dev.', 'pressure_std', float),
        ('Temperature', 'temp', float),
    )


class NORS4(NOR, nmea_utils.DatetimeFix):
    # Sensors Data DF103/DF104
    # Example: $PNORS4,23.6,1530.2,0.0,0.0,0.0,0.000,23.30*66

    fields = (
        ('Battery Voltage', 'battery_voltage', float),
        ('Speed of Sound', 'sound_speed', float),
        ('Heading', 'heading', float),
        ('Pitch', 'pitch', float),
        ('Roll', 'roll', float),
        ('Pressure', 'pressure', float),
        ('Temperature', 'temp', float),
    )


class NORC1(NOR, nmea_utils.DatetimeFix):
    # Current Data DF101/DF102 - NMEA Format 1 and 2
    # Example: $PNORC1,083013,132455,3,11.0,0.332,0.332,0.332,78.9,78.9,78.9,78,78,78*46

    fields = (
        ('Date', 'datestamp', nmea_utils.datestamp),
        ('Time', 'timestamp', nmea_utils.timestamp),
        ('Cell Number', 'cn', int),
        ('Cell Position', 'cp', float),
        ('Velocity X', 'vx', float),
        ('Velocity Y', 'vy', float),
        ('Velocity Z', 'vz', float),
        ('Velocity Z2', 'vz2', float),
        ('Amplitude Beam 1', 'amp1', float),
        ('Amplitude Beam 2', 'amp2', float),
        ('Amplitude Beam 3', 'amp3', float),
        ('Amplitude Beam 4', 'amp4', float),
        ('Correlation Beam 1', 'r1', int),
        ('Correlation Beam 2', 'r2', int),
        ('Correlation Beam 3', 'r3', int),
        ('Correlation Beam 4', 'r4', int),
        ('Correlation Beam 4', 'r5', int),
    )


class NORC4(NOR, nmea_utils.DatetimeFix):
    # Current Data DF103/DF104
    # Example: $PNORC4,1.5,1.395,227.1,32,32*7A

    fields = (
        ('Cell Position', 'cp', float),
        ('Speed', 'sp', float),
        ('Direction', 'dir', float),
        ('Correlation', 'r', int),
        ('Amplitude', 'amp', int),
    )


class NORH4(NOR, nmea_utils.DatetimeFix):
    # Header Data DF103/DF104
    # Example: $PNORH4,161109,143459,0,204C0002*38

    fields = (
        ('Date', 'datestamp', nmea_utils.datestamp),
        ('Time', 'timestamp', nmea_utils.timestamp),
        ('Error Code', 'ec', int),
        ('Status Code', 'sc'),
    )
