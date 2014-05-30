import datetime
import math

def timestamp(s):
    '''
    Converts a timestamp given in "HHMMSS" ASCII format to a
    datetime.time object
    '''
    return datetime.time(
        hour=int(s[0:2]),
        minute=int(s[2:4]),
        second=int(s[4:6]))


def datestamp(s):
    '''
    Converts a datestamp given in "DDMMYY" ASCII format to a
    datetime.datetime object
    '''
    return datetime.datetime.strptime(s, '%d%m%y')


import re
def dm_to_sd(dm):
    '''
    Converts a geographic coordiante given in "degres/minutes" dddmm.mmmm
    format (ie, "12319.943281" = 123 degrees, 19.953281 minutes) to a signed
    decimal (python float) format
    '''
    # '12319.943281'
    if dm == '0':
        return 0
    d, m = re.match('^(\d+)(\d\d\.\d+)$', dm).groups()
    return float(d) + float(m) / 60


class LatLonFix(object):
    '''Mixin to add `lattitude` and `longitude` properties as signed decimals
    to NMEA sentences which have coordiantes given as degrees/minutes (lat, lon)
    and cardinal directions (lat_dir, lon_dir)'''

    @property
    def latitude(self):
        '''Lattitude in signed degrees (python float)'''
        sd = dm_to_sd(self.lat)
        if self.lat_dir == 'N':
            return +sd
        elif self.lat_dir == 'S':
            return -sd

    @property
    def longitude(self):
        '''Longitude in signed degrees (python float)'''
        sd = dm_to_sd(self.lon)
        if self.lon_dir == 'E':
            return +sd
        elif self.lon_dir == 'W':
            return -sd

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
