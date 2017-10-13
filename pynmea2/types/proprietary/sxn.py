'''
Seapath

Message types:

$PSXN,20,horiz-qual,hgt-qual,head-qual,rp-qual*csum term
$PSXN,22,gyro-calib,gyro-offs*csum term
$PSXN,23,roll,pitch,head,heave*csum term
$PSXN,24,roll-rate,pitch-rate,yaw-rate,vertical-vel*csum term
$PSXN,21,event*csum term

Where:

horiz-qual: Horizontal position and velocity quality: 0 = normal, 1 = reduced performance, 2= invalid data.
hgt-qual: Height and vertical velocity quality: 0 = normal, 1 = reduced performance, 2 =invalid data.
head-qual: Heading quality: 0 = normal, 1 = reduced performance, 2 = invalid data.
rp-qual: Roll and pitch quality: 0 = normal, 1 = reduced performance, 2 = invalid data.
gyro-calib: Gyro calibration value since system start-up in degrees on format d.dd.
gyro-offs: Short-term gyro offset in degrees on format d.dd.
roll: Roll in degrees on format d.dd. Positive with port side up.
pitch: Pitch in degrees on format d.dd. Positive with bow up.
heave: Heave in metres on format d.dd. Positive down.
roll-rate: Roll rate in degrees per second on format d.dd. Positive when port side is moving upwards.
pitch-rate: Pitch rate in degrees per second on format d.dd. Positive when bow is moving upwards.
yaw-rate: Yaw rate in degrees per second on format d.dd. Positive when bow is moving towards starboard.
vertical-vel: Vertical velocity in metres per second on format d.dd. Positive when moving downwards.
event: Event code: 1 = system restart.
csum: Checksum (exclusive or) of all characters between, but not including, the preceding $ and * , hexadecimal (00 - FF).
term: CR-LF (2 bytes, values 13 and 10).

Samples:

$PSXN,20,0,0,0,0*3B
$PSXN,23,0.30,-0.97,298.57,0.13*1B
$PSXN,26,0,44.5000,0.7800,-0.9000,NRP*6D

'''
from ... import nmea


class SXN(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[1]
        cls = _cls.sentence_types.get(name, _cls)
        return super(SXN, cls).__new__(cls)


class SXN20(SXN):
    fields = (
        ('Blank', '_blank'),
        ('Message Type', 'message_type', int),
        ('Horizontal position and velocity quality', 'horiz_qual', int),
        ('Height and vertical velocity quality', 'hgt_qual', int),
        ('Heading quality', 'head_qual', int),
        ('Roll and pitch quality', 'rp_qual', int),
    )


class SXN21(SXN):
    fields = (
        ('Blank', '_blank'),
        ('Message Type', 'message_type', int),
        ('Event code: 1 = system restart.', 'event', int),
    )


class SXN22(SXN):
    fields = (
        ('Blank', '_blank'),
        ('Message Type', 'message_type', int),
        ('Gyro calibration value since system start-up in degrees', 'gyro_calib', float),
        ('Short-term gyro offset in degrees', 'gyro_ffs', float),
    )


class SXN23(SXN):
    fields = (
        ('Blank', '_blank'),
        ('Message Type', 'message_type', int),
        ('Roll in degrees. Positive with port side up.', 'roll', float),
        ('Pitch in degrees. Positive with bow up.', 'pitch', float),
        ('Heading, degrees true (0.00 - 359.99).', 'head', float),
        ('Heave in metres. Positive down.', 'heave', float)
    )


class SXN24(SXN):
    fields = (
        ('Blank', '_blank'),
        ('Message Type', 'message_type', int),
        ('Roll rate in degrees/second. Positive when port side is moving upwards.', 'roll_rate', float),
        ('Pitch rate in degrees/second. Positive when bow is moving upwards.', 'pitch_rate', float),
        ('Yaw rate in degrees/second. Positive when bow is moving towards starboard.', 'yaw_rate', float),
        ('Vertical velocity in metres/second. Positive when moving downwards.', 'vertical_vel', float)
    )
