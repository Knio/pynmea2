# Kenwood

from decimal import Decimal
from datetime import date, time

from ... import nmea
from ... import nmea_utils

class KLD(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[0]
        cls = _cls.sentence_types.get(name, _cls)
        return super(KLD, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = manufacturer + data[0]
        super(KLD, self).__init__(manufacturer, data)

class KND(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[0]
        cls = _cls.sentence_types.get(name, _cls)
        return super(KND, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = manufacturer + data[0]
        super(KND, self).__init__(manufacturer, data)

class KLS(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[0]
        cls = _cls.sentence_types.get(name, _cls)
        return super(KLS, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = manufacturer + data[0]
        super(KLS, self).__init__(manufacturer, data)

class KNS(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[0]
        cls = _cls.sentence_types.get(name, _cls)
        return super(KNS, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = manufacturer + data[0]
        super(KNS, self).__init__(manufacturer, data)


class KWD(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        name = manufacturer + data[0]
        cls = _cls.sentence_types.get(name, _cls)
        return super(KWD, cls).__new__(cls)

    def __init__(self, manufacturer, data):
        self.sentence_type = manufacturer + data[0]
        super(KWD, self).__init__(manufacturer, data)


class KWDWPL(KWD, nmea_utils.LatLonFix, nmea_utils.DatetimeFix, nmea_utils.ValidStatusFix):
    """ Kenwood Waypoint Location

    https://github.com/wb2osz/direwolf/blob/master/waypoint.c

    $PKWDWPL,hhmmss,v,ddmm.mm,ns,dddmm.mm,ew,speed,course,ddmmyy,alt,wname,ts*99
    Where,
       hhmmss       is time in UTC from the clock in the transceiver.
                    This will be bogus if the clock was not set properly.
                    It does not use the timestamp from a position
                    report which could be useful.

       GPS Status	A = active, V = void.
                    It looks like this might be modeled after the GPS status values
                    we see in $GPRMC.  i.e. Does the transceiver know its location?
                    I don't see how that information would be relevant in this context.
                    I've observed this under various conditions (No GPS, GPS with/without
                    fix) and it has always been "V."

       ddmm.mm,ns   is latitude. N or S.
       dddmm.mm,ew  is longitude.  E or W.
       speed        is speed over ground, knots.
       course       is course over ground, degrees.
       ddmmyy       is date.  See comments for time.
       alt          is altitude, meters above mean sea level.
       wname        is the waypoint name.  For an Object Report, the id is the object name.
                    For a position report, it is the call of the sending station.
                    An Object name can contain any printable characters.
                    What if object name contains , or * characters?
                    Those are field delimiter characters and it would be unfortunate
                    if they appeared in a NMEA sentence data field.

                    If there is a comma in the name, such as "test,5" the Kenwood TM-D710A displays
                    it fine but we end up with an extra field.

                       $PKWDWPL,150803,V,4237.14,N,07120.83,W,,,190316,,test,5,/'*30

                    If the name contains an asterisk, it doesn't show up on the
                    display and no waypoint sentence is generated.
                    Some other talkers substitute these two characters following the AvMap precedent.

                       $PKWDWPL,204714,V,4237.1400,N,07120.8300,W,,,200316,,test|5,/'*61
                       $PKWDWPL,204719,V,4237.1400,N,07120.8300,W,,,200316,,test~6,/'*6D

       ts           are the table and symbol.

                    What happens if the symbol is comma or asterisk?
                        , Boy Scouts / Girl Scouts
                        * SnowMobile / Snow

                    the D710A just pushes them thru without checking.
                    These would not be parsed properly:

                        $PKWDWPL,150753,V,4237.14,N,07120.83,W,,,190316,,test3,/,*1B
                        $PKWDWPL,150758,V,4237.14,N,07120.83,W,,,190316,,test4,/ **3B

                    Other talkers do the usual substitution and the other end would
                    need to change them back after extracting from NMEA sentence.

                       $PKWDWPL,204704,V,4237.1400,N,07120.8300,W,,,200316,,test3,/|*41
                       $PKWDWPL,204709,V,4237.1400,N,07120.8300,W,,,200316,,test4,/~*49


        *99            is checksum

    Oddly, there is no place for comment.
    """
    fields = (
        ("Subtype", "subtype"),
        ("Time of Receipt", "timestamp", nmea_utils.timestamp),
        ("GPS Status (Void)","status"),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Speed over Ground", "sog", float),
        ("Course over Ground", "cog", float),
        ("Date", "datestamp", nmea_utils.datestamp),
        ("Altitude", "altitude", Decimal),
        ("Waypoint Name", "wname"),
        ("Table and Symbol", "ts"),
    )

class KLDS(KLD, nmea_utils.LatLonFix, nmea_utils.DatetimeFix, nmea_utils.ValidStatusFix):
    """
    $PKLDS,hhmmss,v,ddmm.mm,ns,dddmm.mm,ew,speed,course,ddmmyy,DD.dd,ewSV,fleet,svid,status,fut*99
    $PKLDS,001235,A,3544.6650,N,13940.1900,E,015.0,038.8,110498,10.80,W00,100,2000,15,00,*??
    """
    fields = (
        ("Subtype", "subtype"),
        ("Time of Receipt", "timestamp", nmea_utils.timestamp),
        ("GPS Status (Void)","status"),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Speed over Ground Knot", "sog", float),
        ("Course over Ground", "cog", float),
        ("Date", "datestamp", nmea_utils.datestamp),
        ("Magnetic variation", "declination", float),
        ("Declination Direction", "dec_dir"),
        ("Fleet", "fleet", Decimal),
        ("Sender ID", "senderid"),
        ("Sender Status", "senderstatus", Decimal),
        ("Future Reserved", "future", Decimal),
    )



class KNDS(KND, nmea_utils.LatLonFix, nmea_utils.DatetimeFix, nmea_utils.ValidStatusFix):
    """
    $PKNDS,hhmmss,v,ddmm.mm,ns,dddmm.mm,ew,speed,course,ddmmyy,DD.dd,ewSV,svid,status,fut*99
    $PKNDS,124640,A,4954.1458,N,11923.5992,W,000.0,000.0,120223,19.20,W00,U00002,207,00,*29

    """
    fields = (
        ("Subtype", "subtype"),
        ("Time of Receipt", "timestamp", nmea_utils.timestamp),
        ("GPS Status (Void)","status"),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Speed over Ground Knot", "sog", float),
        ("Course over Ground", "cog", float),
        ("Date", "datestamp", nmea_utils.datestamp),
        ("Magnetic variation", "declination", float),
        ("Declination Direction", "dec_dir"),
        ("Sender ID", "senderid"),
        ("Sender Status", "senderstatus", Decimal),
        ("Future Reserved", "future", Decimal),
    )

class KLSH(KLS, nmea_utils.LatLonFix, nmea_utils.DatetimeFix, nmea_utils.ValidStatusFix):
    """
    $PKLSH,ddmm.mm,ns,dddmm.mm,ew,hhmmss,v,fleet,svid,*99
    $PKLSH,4000.0000,N,13500.0000,E,021720,A,100,2000,* ??
    """
    fields = (
        ("Subtype", "subtype"),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Time of Receipt", "timestamp", nmea_utils.timestamp),
        ("GPS Status (Void)","status"),
        ("Fleet", "fleet", Decimal),
        ("Sender ID", "senderid"),
    )

class KNSH(KNS, nmea_utils.LatLonFix, nmea_utils.DatetimeFix, nmea_utils.ValidStatusFix):
    """
    $PKLSH,ddmm.mm,ns,dddmm.mm,ew,hhmmss,v,svid,*99
    $PKNSH,4000.0000,N,13500.0000,E,021720,A,U00001,* ??
    """
    fields = (
        ("Subtype", "subtype"),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Time of Receipt", "timestamp", nmea_utils.timestamp),
        ("GPS Status (Void)","status"),
        ("Sender ID", "senderid"),
    )

