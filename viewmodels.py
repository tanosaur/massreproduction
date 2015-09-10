from PyQt4.QtGui import QItemDelegate, QComboBox
from PyQt4.QtCore import QObject, SIGNAL, SLOT, pyqtSignal, pyqtSlot
from models import BinSizeRecord, Ion, Range

from collections import namedtuple

FinalPlotRecord = namedtuple('FinalPlotRecord', 'm2cs bin_size committed_analyses')
WorkingPlotRecord = namedtuple('WorkingPlotRecord', 'm2cs bin_size all_analyses ions')
MethodsRecord = namedtuple('MethodsRecord', 'ion methods m2cs bin_size')
MRRecord = namedtuple('MRRecord', 'analyses metadata')

class MethodsViewModel(QObject):

    def __init__(self):
        super(MethodsViewModel, self).__init__(None)

        self._record = MethodsRecord(
            ion=None,
            methods={},
            m2cs=(),
            bin_size=BinSizeRecord(1, 0, 1),
            )

    @pyqtSlot(dict)
    def on_methods_updated(self, new_methods):
        self._record = self._record._replace(methods=new_methods)

    @pyqtSlot(tuple)
    def on_m2cs_updated(self, new_m2cs):
        self._record = self._record._replace(m2cs=new_m2cs)

    @pyqtSlot(BinSizeRecord)
    def on_bin_size_updated(self, new_bin_size):
        self._record = self._record._replace(bin_size=new_bin_size)

    def run_method_for_ion(self, new_ion, method_name):
        self._record = self._record._replace(ion=new_ion)
        module = self._record.methods[method_name]

        method_to_call = getattr(module, method_name.lower())
        required_inputs = module.required_inputs()
        inputs = self._send_inputs(required_inputs)
        start, end = method_to_call(*inputs)
        return Range(start, end)

    def _send_inputs(self, required_inputs):
        input_reference={
            'suggested_m2c': self._record.ion.mass_to_charge,
            'abundance': self._record.ion.isotope.abundance,
            'bin_size': self._record.bin_size.value,
            'm2cs': self._record.m2cs,
        }
        inputs = []

        for _input in required_inputs:
            if _input in input_reference:
                inputs.append(input_reference[_input])

        return inputs

class MRViewModel(QObject):
    def __init__(self):
        super(MRViewModel, self).__init__(None)

        self._record = MRRecord(
            analyses=(),
            metadata=()
            )

    @pyqtSlot(tuple)
    def on_metadata_updated(self, new_metadata):
        self._record = self.record._replace(metadata=new_metadata)
        self.updated.emit(self._record)

    @pyqtSlot(dict)
    def on_analyses_updated(self, new_analyses):
        self._record = self._record._replace(analyses=new_analyses)
        self.updated.emit(self._record)


class WorkingPlotViewModel(QObject):
    updated = pyqtSignal(WorkingPlotRecord)

    def __init__(self):
        super(WorkingPlotViewModel, self).__init__(None)

        self._record = WorkingPlotRecord(
            m2cs=(),
            bin_size=BinSizeRecord(1, 0, 1),
            all_analyses={},
            ions=()
        )

    @pyqtSlot(tuple)
    def on_m2cs_updated(self, new_m2cs):
        self._record = self._record._replace(m2cs=new_m2cs)
        self.updated.emit(self._record)

    @pyqtSlot(BinSizeRecord)
    def on_bin_size_updated(self, new_bin_size):
        self._record = self._record._replace(bin_size=new_bin_size)
        self.updated.emit(self._record)

    @pyqtSlot(tuple)
    def on_all_analyses_updated(self, new_analyses):
        self._record = self._record._replace(all_analyses=new_analyses)
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
            m2cs=(),
            bin_size=BinSizeRecord(1, 0, 1),
            committed_analyses={},
        )

    @pyqtSlot(tuple)
    def on_m2cs_updated(self, new_m2cs):
        self._record = self._record._replace(m2cs=new_m2cs)
        self.updated.emit(self._record)

    @pyqtSlot(BinSizeRecord)
    def on_bin_size_updated(self, new_bin_size):
        self._record = self._record._replace(bin_size=new_bin_size)
        self.updated.emit(self._record)

    @pyqtSlot(tuple)
    def on_committed_analyses_updated(self, new_analyses):
        self._record = self._record._replace(committed_analyses=new_analyses)
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
