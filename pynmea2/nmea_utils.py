#pylint: disable=invalid-name
import datetime
import re


# python 2.7 backport
if not hasattr(datetime, 'timezone'):
    class UTC(datetime.tzinfo):
        def utcoffset(self, dt):
            return datetime.timedelta(0)
    class timezone(object):
        utc = UTC()
    datetime.timezone = timezone


def valid(s):
    return s == 'A'


def timestamp(s):
    '''
    Converts a timestamp given in "hhmmss[.ss]" ASCII text format to a
    datetime.time object
    '''
    ms_s = s[6:]
    ms = ms_s and int(float(ms_s) * 1000000) or 0

    t = datetime.time(
        hour=int(s[0:2]),
        minute=int(s[2:4]),
        second=int(s[4:6]),
        microsecond=ms,
        tzinfo=datetime.timezone.utc)
    return t


def datestamp(s):
    '''
    Converts a datestamp given in "DDMMYY" ASCII text format to a
    datetime.datetime object
    '''
    return datetime.datetime.strptime(s, '%d%m%y').date()


def dm_to_sd(dm):
    '''
    Converts a geographic co-ordinate given in "degrees/minutes" dddmm.mmmm
    format (eg, "12319.943281" = 123 degrees, 19.943281 minutes) to a signed
    decimal (python float) format
    '''
    # '12319.943281'
    if not dm or dm == '0':
        return 0.
    r = re.match(r'^(\d+)(\d\d\.\d+)$', dm)
    if not r:
        raise ValueError("Geographic coordinate value '{}' is not valid DDDMM.MMM".format(dm))
    d, m = r.groups()
    return float(d) + float(m) / 60


class LatLonFix(object):
    '''Mixin to add `latitude` and `longitude` properties as signed decimals
    to NMEA sentences which have co-ordinates given as degrees/minutes (lat, lon)
    and cardinal directions (lat_dir, lon_dir)'''
    #pylint: disable=no-member
    @property
    def latitude(self):
        '''Latitude in signed degrees (python float)'''
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


class ValidRMCStatusFix(ValidStatusFix):
    #pylint: disable=no-member
    @property
    def is_valid(self):
        status = super(ValidRMCStatusFix, self).is_valid
        if self.name_to_idx["mode_indicator"] < len(self.data):
            status &= self.mode_indicator in tuple('ADEFMPRS')
        if self.name_to_idx["nav_status"] < len(self.data):
            status &= self.nav_status in tuple('SCU')
        return status


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
