#pylint: disable=invalid-name
import datetime

def timestamp(s):
    '''
    Converts a timestamp given in "hhmmss[.ss]" ASCII format to a
    datetime.time object
    '''
    ms = (len(s) == 9) and 10000 * int(s[7:9]) or 0

    t = datetime.time(
        hour=int(s[0:2]),
        minute=int(s[2:4]),
        second=int(s[4:6]),
        microsecond=ms)
    return t


def datestamp(s):
    '''
    Converts a datestamp given in "DDMMYY" ASCII format to a
    datetime.datetime object
    '''
    return datetime.datetime.strptime(s, '%d%m%y').date()


import re
def dm_to_sd(dm):
    '''
    Converts a geographic coordiante given in "degres/minutes" dddmm.mmmm
    format (ie, "12319.943281" = 123 degrees, 19.953281 minutes) to a signed
    decimal (python float) format
    '''
    # '12319.943281'
    if not dm or dm == '0':
        return 0.
    d, m = re.match(r'^(\d+)(\d\d\.\d+)$', dm).groups()
    return float(d) + float(m) / 60


class LatLonFix(object):
    '''Mixin to add `lattitude` and `longitude` properties as signed decimals
    to NMEA sentences which have coordiantes given as degrees/minutes (lat, lon)
    and cardinal directions (lat_dir, lon_dir)'''
    #pylint: disable=no-member
    @property
    def latitude(self):
        '''Lattitude in signed degrees (python float)'''
        sd = dm_to_sd(self.lat)
        if self.lat_dir == 'N':
            return +sd
        elif self.lat_dir == 'S':
            return -sd
        else:
            return 0.

    @property
    def longitude(self):
        '''Longitude in signed degrees (python float)'''
        sd = dm_to_sd(self.lon)
        if self.lon_dir == 'E':
            return +sd
        elif self.lon_dir == 'W':
            return -sd
        else:
            return 0.

    @staticmethod
    def _minutes(x):
        return abs(x * 60.) % 60.

    @staticmethod
    def _seconds(x):
        return abs(x * 3600.) % 60.

    @property
    def latitude_minutes(self):
        return self._minutes(self.latitude)

    @property
    def longitude_minutes(self):
        return self._minutes(self.longitude)

    @property
    def latitude_seconds(self):
        return self._seconds(self.latitude)

    @property
    def longitude_seconds(self):
        return self._seconds(self.longitude)


class DatetimeFix(object):
    #pylint: disable=no-member
    @property
    def datetime(self):
        return datetime.datetime.combine(self.datestamp, self.timestamp)


class ValidStatusFix(object):
    #pylint: disable=no-member
    @property
    def is_valid(self):
        return self.status == 'A'


class ValidGSAFix(object):
    #pylint: disable=no-member
    @property
    def is_valid(self):
        return int(self.mode_fix_type) in [2, 3]


class ValidGGAFix(object):
    #pylint: disable=no-member
    @property
    def is_valid(self):
        return self.gps_qual in range(1,6)


class ValidVBWFix(object):
    #pylint: disable=no-member
    @property
    def is_valid(self):
        return self.data_validity_water_spd == self.data_validity_grnd_spd == 'A'


class TZInfo(datetime.tzinfo):
    def __init__(self, hh, mm):
        self.hh = hh
        self.mm = mm
        super(TZInfo, self).__init__()

    def tzname(self, dt):
        return ''

    def dst(self, dt):
        return datetime.timedelta(0)

    def utcoffset(self, dt):
        return datetime.timedelta(hours=self.hh, minutes=self.mm)
