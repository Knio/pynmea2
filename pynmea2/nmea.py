import re
import operator


class NMEASentence(object):
    '''
    Base NMEA Sentence

    Parses and generates NMEA strings

    Examples:

    >>> s = NMEASentence.parse("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D")
    >>> print s


    Sentence types are implemented as
    '''

    class __metaclass__(type):
        def __init__(cls, name, bases, dict):
            type.__init__(cls, name, bases, dict)
            if 'NMEASentence' in [b.__name__ for b in bases]:
                sentence_type = name.replace('Sentence', '')
                NMEASentence._sentence_types[name] = cls
                cls.sentence_type = name
                cls.name_to_idx = {f[1]:i for i,f in enumerate(cls.fields)}

    _sentence_types = {}

    _re = re.compile('''
        ^[^$]*\$?
        (?P<nmea_str>
            (?P<talker>\w{2})
            (?P<sentence_type>\w{3}),
            (?P<data>[^*]+)
        )(?:\\*(?P<checksum>[A-F0-9]{2}))
        [\\\r\\\n]*
        ''', re.X | re.IGNORECASE)

    # This regex shoehorns a generic proprietary sentence match into
    # the existing parser to avoid duplicating code. Thus the `talker`
    # and `checksum` groups are always empty dummy matches to ensure
    # the remainder of the parsing code can be used with minimal
    # changes.
    _re_proprietary = re.compile('''
        ^[^$]*\$?
        (?P<nmea_str>
            (?P<talker>)
            (?P<sentence_type>P)
            (?P<data>(?P<manufacturer>\w{3})[^$]+)
        )(?:\\*(?P<checksum>))?
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

        A proprietary sentence without a custom implementation is
        returned as an instance of a generic proprietary sentence class.

        Raises ValueError if the string could not be parsed, or if the checksum
        did not match.

        Note: A checksum check is not performed for proprietary
              sentences without a custom implementation.
        '''
        match = NMEASentence._re.match(data) or NMEASentence._re_proprietary.match(data)
        if not match:
            raise ValueError('could not parse data: %r' % data)

        nmea_str        = match.group('nmea_str')
        talker          = match.group('talker').upper()
        sentence_type   = match.group('sentence_type').upper()
        data            = match.group('data').split(',') if sentence_type != "P" else (match.group('data'),)
        checksum        = match.group('checksum')

        if checksum:
            # print nmea_str
            cs1 = int(checksum, 16)
            cs2 = NMEASentence.checksum(nmea_str)
            if cs1 != cs2:
                raise ValueError('checksum does not match: %02X != %02X' %
                    (cs1, cs2))

        cls = NMEASentence._sentence_types.get(sentence_type, None)
        if not cls:
            raise ValueError('Unknown sentence type %s' % sentence_type)

        return cls(talker, sentence_type, *data)

    def __init__(self, talker, sentence_type, *data):
        self.talker = talker
        self.type = sentence_type
        self.data = list(data)

    def __getattr__(self, name):
        t = type(self)
        i = t.name_to_idx[name]
        f = t.fields[i]
        v = self.data[i]
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
