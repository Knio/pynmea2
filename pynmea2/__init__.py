from ._version import __version__
version = __version__

from .nmea import NMEASentence, ProprietarySentence, ChecksumError, ParseError, SentenceTypeError
from .types import *
from .stream import NMEAStreamReader

parse = NMEASentence.parse
