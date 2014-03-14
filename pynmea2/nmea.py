import re
import operator
from functools import reduce


class NMEASentenceType(type):
    sentence_types = {}
    def __init__(cls, name, bases, dict):
        type.__init__(cls, name, bases, dict)
        if not hasattr(cls, 'fields'):
            return
        # print cls, id(cls.sentence_types)
        cls.sentence_types[name] = cls
        cls.sentence_type = name
        cls.name_to_idx = {f[1]:i for i,f in enumerate(cls.fields)}


# http://mikewatkins.ca/2008/11/29/python-2-and-3-metaclasses/
NMEASentenceBase = NMEASentenceType('NMEASentenceBase', (object,), {})


class NMEASentence(NMEASentenceBase):
    '''
    Base NMEA Sentence

    Parses and generates NMEA strings

    Examples:

    >>> s = NMEASentence.parse("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D")
    >>> print(s)
    '''

    _re = re.compile('''
        ^[^$]*\$?
        (?P<nmea_str>(
            ((?P<talker_talker>\w{2})(?P<talker_sentence_type>\w{3}))|
            (P(?P<proprietary_sentence_manufacturer>\w{3})(?P<proprietary_sentence_type>\w+))|
            ((?P<query_talker>\w{2})(?P<query_requester>\w{2})Q,(?P<query_sentence_type>\w{3}))
            ),(?P<data>[^*]+)
        )(?:\\*(?P<checksum>[A-F0-9]{2}))
        [\\\r\\\n]*
        ''', re.X | re.IGNORECASE)

    @staticmethod
    def checksum(nmea_str):
        return reduce(operator.xor, map(ord, nmea_str), 0)

    @staticmethod
    def parse(data):
        '''
        parse(data)

        Parses a string representing a NMEA 0183 sentence, and returns a
        NMEASentence object

        Raises ValueError if the string could not be parsed, or if the checksum
        did not match.
        '''
        match = NMEASentence._re.match(data)
        if not match:
            raise ValueError('could not parse data: %r' % data)


        nmea_str        = match.group('nmea_str')
        data            = tuple(match.group('data').split(','))
        checksum        = match.group('checksum')
        
        talker_talker   = match.group('talker_talker')
        sentence_type   = match.group('talker_sentence_type')
        
        proprietary_sentence_manufacturer \
                        = match.group('proprietary_sentence_manufacturer')
        proprietary_sentence_type \
                        = match.group('proprietary_sentence_type')
        
        query_talker    = match.group('query_talker')
        query_requester = match.group('query_requester')
        query_sentence_type \
                        = match.group('query_sentence_type')

        if checksum:
            # print nmea_str
            cs1 = int(checksum, 16)
            cs2 = NMEASentence.checksum(nmea_str)
            if cs1 != cs2:
                raise ValueError('checksum does not match: %02X != %02X' %
                    (cs1, cs2))

        
        if talker_talker:
            key = (
                talker_talker.upper(),
                sentence_type.upper()
            )
            cls = TalkerSentence.sentence_types[key[1]]
            data = key + data

        elif query_talker:
            key = (
                query_talker.upper(),
                query_sentence_type.upper()
            )
            cls = QuerySentence.sentence_types[key]
            data = (
                query_talker.upper(),
                query_requester.upper(),
                query_sentence_type.upper(),
            ) + data

        elif proprietary_sentence_manufacturer:
            key = (
                proprietary_sentence_manufacturer.upper(),
                proprietary_sentence_type.upper(),
            )
            cls = ProprietarySentence.sentence_types[''.join(key)]
            data = key + data

        else:
            raise ValueError('Unknown sentence type %s' % sentence_type)

        return cls(*data)

    def __getattr__(self, name):
        t = type(self)
        i = t.name_to_idx[name]
        f = t.fields[i]
        if i < len(self.data):
            v = self.data[i]
        else:
            v = None
        if len(f) >= 3:
            if v == '':
                return None
            return f[2](v)
        else:
            return v

    def __setattr__(self, name, value):
        t = type(self)
        if name not in t.name_to_idx:
            return object.__setattr__(self, name, value)

        i = t.name_to_idx[name]
        self.data[i] = str(value)

    def __repr__(self):
        r = []
        d = []
        t = type(self)
        for i, v in enumerate(self.data):
            if i >= len(t.fields):
                d.append(v)
                continue
            name = t.fields[i][1]
            r.append('%s=%r' % (name, getattr(self, name)))

        return '<%s(%s)%s>' % (
            type(self).__name__,
            ', '.join(r),
            d and ' data=%r' % d or ''
        )

    def render(self, checksum=True, dollar=True, newline=False):
        res = self.talker + self.sentence_type + ','
        res += ','.join(self.data)
        if checksum:
            res += '*%02X' % NMEASentence.checksum(res)
        if dollar:
            res = '$' + res
        if newline:
            res += (newline is True) and '\r\n' or newline
        return res


    def __str__(self):
        return self.render()


class TalkerSentence(NMEASentence):
    sentence_types = {}
    def __init__(self, talker, sentence_type, *data):
        self.talker = talker
        self.sentence_type = sentence_type
        self.data = list(data)


class QuerySentence(NMEASentence):
    sentence_types = {}
    def __init__(self, talker, listener, sentence_type, *data):
        self.talker = talker
        self.listener = listener
        self.sentence_type = sentence_type
        self.data = list(data)


class ProprietarySentence(NMEASentence):
    sentence_types = {}
    def __init__(self, manufacturer, sentence_type, *data):
        self.manufacturer = manufacturer
        self.sentence_type = sentence_type
        self.data = list(data)
