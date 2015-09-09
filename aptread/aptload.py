
import numpy as np

from . import posload as pl
from . import eposload as epl

# === Exceptions ===
class APReadError(Exception): pass
class InvalidRngError(Exception): pass
class InvalidIndexError(Exception): pass

# === Class defs ===
class POSData():
    def __init__(self, pospath):
        try:
            self.pos = pl.POS(pospath)
        except pl.ReadError:
            raise APReadError('Error opening pos file %s' % pospath)
            return

class EPOSData():
    def __init__(self, epospath):
        try:
            self.epos = epl.EPOS(epospath)
        except epl.ReadError:
            raise APReadError('Error opening epos file %s' % epospath)
            return
