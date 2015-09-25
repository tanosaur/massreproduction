from PyQt4.QtGui import QItemDelegate, QComboBox
from PyQt4.QtCore import QObject, SIGNAL, SLOT, pyqtSignal, pyqtSlot
from models import BinSizeRecord, Ion, Range, ExperimentInfo, Analysis, Isotope, ISOTOPES
import json
import datetime
from collections import namedtuple

WorkingPlotRecord = namedtuple('WorkingPlotRecord', 'm2cs bin_size analyses ions')
MethodsRecord = namedtuple('MethodsRecord', 'methods m2cs bin_size')
MRRecord = namedtuple('MRRecord', 'analyses metadata')
AnalysesRecord = namedtuple('AnalysesRecord', 'analyses methods')

class MethodsViewModel(QObject):

    def __init__(self):
        super(MethodsViewModel, self).__init__(None)

        self._record = MethodsRecord(
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
        module = self._record.methods[method_name]
        method_to_call = getattr(module, method_name.lower())

        required_inputs = module.required_inputs()
        inputs = self._send_inputs(required_inputs, new_ion)
        start, end = method_to_call(*inputs)
        return Range(start, end)

    def _send_inputs(self, required_inputs, ion):
        input_reference={
            'suggested_m2c': ion.mass_to_charge,
            'abundance': ion.isotope.abundance,
            'bin_size': self._record.bin_size.value,
            'm2cs': self._record.m2cs,
        }
        inputs = []

        for _input in required_inputs:
            if _input in input_reference:
                inputs.append(input_reference[_input])

        return inputs

class MRViewModel(QObject):
    export_error = pyqtSignal()
    updated = pyqtSignal()

    def __init__(self):
        super(MRViewModel, self).__init__(None)

        self._record = MRRecord(
            analyses=(),
            metadata=()
            )

    @pyqtSlot(tuple)
    def on_metadata_updated(self, new_metadata):
        self._record = self._record._replace(metadata=new_metadata)

    @pyqtSlot(dict)
    def on_analyses_updated(self, new_analyses):
        self._record = self._record._replace(analyses=new_analyses)

    def check_manual_analyses_have_reasons(self):
        for ion, analysis in self._record.analyses.items():
            if analysis.method == 'Manual' and analysis.reason == None:
                self.export_error.emit()
                return False

        return True

    def export_analyses_to_mrfile(self, filename):
        if self._record:
            if self.check_manual_analyses_have_reasons():
                record = self._to_json(self._record)
                with open(filename, mode='w', encoding='utf-8') as f:
                    json.dump(record, f, indent=2)

    def _to_json(self, record):
        analyses_list = []

        analyses_list.append([
            record.metadata.ID,
            record.metadata.description
            ])

        for ion, analysis in record.analyses.items():
            analyses_list.append(ion.name)
            analyses_list.append({
            'Ion': [ion.isotope.element, ion.isotope.number, ion.isotope.mass, ion.isotope.abundance, ion.charge_state],
            'Method': analysis.method,
            'Range': [analysis.range.start, analysis.range.end],
            'Reason': analysis.reason,
            'Color': analysis.color,
            })

        analyses_list.append(str(datetime.datetime.today())) #ISO 8601 format

        return analyses_list

    def import_analyses_from_mrfile(self, mrfile):
        with open(mrfile, 'r', encoding='utf-8') as f:
            contents = json.load(f)

        new_analyses, new_metadata = self._from_json(contents)

        return new_analyses, new_metadata

    def _from_json(self, contents):
        new_analyses = {}
        new_metadata = None

        for entry in contents:
            if isinstance(entry, list):
                new_metadata = ExperimentInfo(entry[0], entry[1])
            if isinstance(entry, dict):
                element, number, mass, abundance, charge_state = entry.get('Ion')
                method_name = entry.get('Method')
                start, end = entry.get('Range')
                reason = entry.get('Reason')
                color = entry.get('Color')

                _range = Range(start, end)

                new_analyses.update({Ion(Isotope(element, number, mass, abundance), charge_state): Analysis(method_name, _range, reason, color)})

        return new_analyses, new_metadata

class WorkingPlotViewModel(QObject):
    updated = pyqtSignal(WorkingPlotRecord)

    def __init__(self):
        super(WorkingPlotViewModel, self).__init__(None)

        self._record = WorkingPlotRecord(
            m2cs=(),
            bin_size=BinSizeRecord(1, 0, 1),
            analyses={},
            ions=(),
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
    def on_analyses_updated(self, new_analyses):
        self._record = self._record._replace(analyses=new_analyses)
        self.updated.emit(self._record)

    @pyqtSlot(tuple)
    def on_ions_updated(self, new_ions):
        self._record = self._record._replace(ions=new_ions)
        self.updated.emit(self._record)

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
