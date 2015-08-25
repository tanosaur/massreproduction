from collections import namedtuple
import unittest
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot

ELEMENTS = (
    'Al', 'H'
)

Isotope = namedtuple('Isotope', 'element number mass abundance')
ISOTOPES = [
    Isotope('Al', 27, 26.98, 100),
    Isotope('Cr', 50, 49.95, 4.3),
    Isotope('Cr', 52, 51.94, 83.8),
    Isotope('Cr', 53, 52.94, 9.5),
    Isotope('Cr', 54, 53.94, 2.4),
    Isotope('H', 1, 1.008, 99.985),
    Isotope('H', 2, 2.014, 0.015),
]

class Ion(namedtuple('Ion', 'isotope charge_state')):
    @property
    def mass_to_charge(self):
        return self.isotope.mass / self.charge_state

    @property
    def name(self):
        return "%s%s+%s".format(self.isotope.number, self.isotope.element, self.charge_state)

Range = namedtuple('Range', 'ion start end')
WorkingPlotRecord = namedtuple('WorkingPlotRecord', 'm2c bin_size ranges ions')
BinSizeRecord = namedtuple('BinSizeRecord', 'maximum minimum value')
Trace = namedtuple('Trace', 'method reason')
FinalPlotRecord = namedtuple('FinalPlotRecord', 'm2c bin_size ranges')

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

class SuggestedIonsViewModel(QObject):
    updated = pyqtSignal(tuple) # (Ion, ...)

    def __init__(self):
        super(SuggestedIonsViewModel, self).__init__(None)

        self._record = ()

    @pyqtSlot(tuple)
    def on_ions_updated(self, new_ions):
        self._record = new_ions
        self.updated.emit(self._record)

class AnalysesTableViewModel(QObject):
    updated = pyqtSignal(dict) # Range: Trace

    def __init__(self):
        super(AnalysesTableViewModel, self).__init__(None)

        self._record = {}

    @pyqtSlot(tuple)
    def on_analyses_updated(self, new_analyses):
        self._record = new_analyses
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

class LoadedM2CModel(QObject):
    updated = pyqtSignal(tuple)

    def __init__(self):
        super(LoadedM2CModel, self).__init__(None)

        self._m2cs=()

    def replace(self, new_m2cs):
        old_m2cs = self._m2cs
        self._m2cs = new_m2cs

        self.updated.emit(self._m2cs)

        return old_m2cs

    def prime(self):
        self.updated.emit(self._m2cs)

class BinSizeModel(QObject):
    updated = pyqtSignal(BinSizeRecord)

    def __init__(self):
        super(BinSizeModel, self).__init__(None)

        self._record = BinSizeRecord(
            maximum = 9000,
            minimum = 0,
            value = 1000
        )

    def replace_value(self, new_value): #TODO throw exception for new_bin_size > max, < min
        old_record = self._record
        self._record = self._record._replace(value=new_value)

        self.updated.emit(self._record)

        return old_record

    def prime(self):
        self.updated.emit(self._record)

class AllRangesModel(QObject):
    updated = pyqtSignal(tuple)

    def __init__(self):
        super(AllRangesModel, self).__init__(None)

        self._allranges = ()

    def replace(self, new_allranges):
        old_allranges = self._allranges
        self._allranges = new_allranges

        self.updated.emit(self._allranges)

        return old_allranges

class CommittedRangesModel(QObject):
    updated = pyqtSignal(tuple)

    def __init__(self):
        super(CommittedRangesModel, self).__init__(None)

        self._ranges=()
        self._committedranges = ()

    @pyqtSlot(tuple)
    def on_ranges_updated(self, new_ranges):
        self._ranges = new_ranges
        set(self._committedranges).intersection_update(set(self._ranges))
        self.updated.emit(self._committedranges)

    def commit(self, new_committedranges):
        self._committedranges = new_committedranges
        self.updated.emit(self._committedranges)

# range_a = Range()
# range_b = Range()
# range_c = Range()
#
# model = CommittedRangesModel()
# model.on_ranges_updated((range_a, range_b))
# model.commit((range_a,))
#
# # NOW emit will emit updated, with (range_a, )
#
# model.on_ranges_updated((range_a, range_b, range_c))
# model.commit((range_a, range_c))
#
# # NOW emit will emit updated, with (range_a, range_c)
#
# model.on_ranges_updated((range_b, range_c))
#
# # NOW emit will emit updated, with (range_c)


class SuggestedIonsModel(QObject):
    updated = pyqtSignal(tuple)

    def __init__(self):
        super(SuggestedIonsModel, self).__init__(None)

        self._suggested_ions = ()

    def replace(self, new_suggested_ions):
        old_suggested_ions = self._suggested_ions
        self._suggested_ions = new_suggested_ions

        self.updated.emit(self._suggested_ions)

        return old_suggested_ions

class AnalysesModel(QObject):
    updated = pyqtSignal(dict)

    def __init__(self):
        super(AnalysesModel, self).__init__(None)

        self._analyses = {}

    def replace(self, new_analyses):
        old_analyses = self._analyses
        self._analyses = new_analyses

        self.updated.emit(self._analyses)

        return old_analyses

class TestModels(unittest.TestCase):

    def CommittedRangesModel_with_committed_ranges(self):
        committed_ranges_model=CommittedRangesModel()
        range_a=Range(1,2,3)
        range_b=Range(1,3,4)
        ranges=(range_a, range_b)
        committed_ranges_model.commit(range_a)
        all_ranges_model=AllRangesModel()
        all_ranges_model.replace(ranges)
        self.assertTrue()


if __name__ == '__main__':
    unittest.main()
