import unittest
import numpy as np

from PyQt4.QtCore import QObject, pyqtSignal

class Commands(QObject):
    def __init__(self, parent=None):
        super(Commands, self).__init__(parent)

    def load(self, rngmethod):
        self.dataset.load(m2c, length)
