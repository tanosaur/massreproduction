from PyQt4.QtGui import QItemDelegate, QComboBox
from PyQt4.QtCore import QObject, SIGNAL, SLOT, pyqtSignal, pyqtSlot
from models import BinSizeRecord

from collections import namedtuple

FinalPlotRecord = namedtuple('FinalPlotRecord', 'm2c bin_size ranges')
WorkingPlotRecord = namedtuple('WorkingPlotRecord', 'm2c bin_size ranges ions')

class WorkingPlotViewModel(QObject):
    updated = pyqtSignal(WorkingPlotRecord)

    def __init__(self):
        super(WorkingPlotViewModel, self).__init__(None)

        self._record = WorkingPlotRecord(
            m2c=(),
            bin_size=BinSizeRecord(1, 0, 1),
            ranges=(),
            ions=()
        )

    @pyqtSlot(tuple)
    def on_m2c_updated(self, new_m2c):
        self._record = self._record._replace(m2c=new_m2c)
        self.updated.emit(self._record)

    @pyqtSlot(BinSizeRecord)
    def on_bin_size_updated(self, new_bin_size):
        self._record = self._record._replace(bin_size=new_bin_size)
        self.updated.emit(self._record)

    @pyqtSlot(tuple)
    def on_ranges_updated(self, new_ranges):
        self._record = self._record._replace(ranges=new_ranges)
        self.updated.emit(self._record)

    @pyqtSlot(tuple)
    def on_ions_updated(self, new_ions):
        self._record = self._record._replace(ions=new_ions)
        self.updated.emit(self._record)

class FinalPlotViewModel(QObject):
    updated = pyqtSignal(FinalPlotRecord)

    def __init__(self):
        super(FinalPlotViewModel, self).__init__(None)

        self._record = FinalPlotRecord(
            m2c=(),
            bin_size=BinSizeRecord(1, 0, 1),
            ranges=(),
        )

    @pyqtSlot(tuple)
    def on_m2c_updated(self, new_m2c):
        self._record = self._record._replace(m2c=new_m2c)
        self.updated.emit(self._record)

    @pyqtSlot(BinSizeRecord)
    def on_bin_size_updated(self, new_bin_size):
        self._record = self._record._replace(bin_size=new_bin_size)
        self.updated.emit(self._record)

    @pyqtSlot(tuple)
    def on_ranges_updated(self, new_ranges):
        self._record = self._record._replace(ranges=new_ranges)
        self.updated.emit(self._record)

AnalysesRecord = namedtuple('AnalysesRecord', 'analyses methods')

class AnalysesViewModel(QObject):
    updated = pyqtSignal(AnalysesRecord)

    def __init__(self):
        super(AnalysesViewModel, self).__init__(None)

        self._record = AnalysesRecord(
            analyses = {},
            methods = (),
        )

    @pyqtSlot(dict)
    def on_analyses_updated(self, new_analyses):
        self._record = self._record._replace(analyses=new_analyses)
        self.updated.emit(self._record)

    @pyqtSlot(tuple)
    def on_methods_updated(self, new_methods):
        self._record = self._record._replace(methods=new_methods)
        self.updated.emit(self._record)
