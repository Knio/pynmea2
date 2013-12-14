version = __version__ = '0.5.1'

from nmea import NMEASentence
from types import *
from stream import NMEAStreamReader


parse = NMEASentence.parse
