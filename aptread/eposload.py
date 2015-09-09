# =============================================================================
# (C) Copyright 2015
# Australian Centre for Microscopy & Microanalysis
# The University of Sydney
# =============================================================================
# File:   eposload.py
# Date:   2014-09-09
# Author: Tong Gao & Clara Tan
#
# Description:
# EPOS data loader classes
# =============================================================================

import numpy as np

class ReadError(Exception): pass

# class EPOS():
#     def __init__(self, epospath):
#         self.xyz, self.mc = self.loadfile(epospath)

def loadfile(fn):
    try:
        with open(fn, 'rb') as content_file:
            epos_raw = content_file.read()
    except (IOError, OSError):
        raise ReadError('Error opening epos file %s' % fn)
        return

    epos_array = np.ndarray((len(epos_raw)/11,), dtype='>f', buffer=epos_raw)
    epos = np.reshape(epos_array, (-1, 11))
    # self.xyz = epos[:,0:3]
    # self.mc = epos[:,3]
    # return self.xyz, self.mc

loadfile('/Users/sojung/OneDrive/MassRep/data/R14_14153-v01.epos')
