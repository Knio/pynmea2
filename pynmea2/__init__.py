version = __version__ = '0.6.0'

from .nmea import NMEASentence
from .types import *
from .stream import NMEAStreamReader


parse = NMEASentence.parse
