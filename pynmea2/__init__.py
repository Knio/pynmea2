from ._version import __version__
version = __version__

from .nmea import NMEASentence, ProprietarySentence, QuerySentence
from .nmea import ChecksumError, ParseError, SentenceTypeError

from .types import *
from .stream import NMEAStreamReader

parse = NMEASentence.parse
