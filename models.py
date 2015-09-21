from collections import namedtuple
import unittest
import json
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot

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
        return '%s%s+%s' % (self.isotope.number, self.isotope.element, self.charge_state)

Range = namedtuple('Range', 'start end')
Analysis = namedtuple('Analysis', 'method range reason color')
BinSizeRecord = namedtuple('BinSizeRecord', 'maximum minimum value')
ExperimentInfo = namedtuple('Experiment', 'ID description')

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

    def prime(self):
        self.updated.emit(self._suggested_ions)

class MethodsModel(QObject):
    updated = pyqtSignal(dict)

    def __init__(self):
        super(MethodsModel, self).__init__(None)

        self._methods = {}

    def replace(self, new_methods):
        self._methods = new_methods
        self.updated.emit(self._methods)

    def prime(self):
        self.updated.emit(self._methods)

class CommittedAnalysesModel(QObject):
    updated = pyqtSignal(tuple)

    def __init__(self):
        super(CommittedAnalysesModel, self).__init__(None)

        self._ranges=()
        self._committedranges = ()

    @pyqtSlot(tuple)
    def on_all_analyses_updated(self, new_ranges):
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
# model = CommittedAnalysesModel()
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

class AllAnalysesModel(QObject):
    updated = pyqtSignal(dict)

    def __init__(self):
        super(AllAnalysesModel, self).__init__(None)

        self._analyses = {}

    def append(self, new_analyses):
        old_analyses = self._analyses.copy()

        self._analyses.update(new_analyses)
        self.updated.emit(self._analyses)

        return old_analyses

    def replace(self, new_analyses):
        self._analyses = new_analyses
        self.updated.emit(self._analyses)

    def update_method_for_ion(self, ion, method, _range):
        old_analysis = self._analyses[ion]
        self._analyses[ion] = old_analysis._replace(
            method=method,
            range=_range)
        self.updated.emit(self._analyses)

        return ion, old_analysis.method, old_analysis.range

    def update_manual_range_for_ion(self, ion, _range):
        old_analysis = self._analyses[ion]
        self._analyses[ion] = old_analysis._replace(
            range=_range)
        self.updated.emit(self._analyses)

        return ion, old_analysis.range

    def export_analyses_to_mrfile(self):
        analyses = self._to_json(self._analyses)
        with open('please.mr', mode='w', encoding='utf-8') as f:
            json.dump(analyses, f, indent=2)

    def _to_json(self, analyses):
        analyses_list = []
        for ion, analysis in analyses.items():
            analyses_list.append(ion.name)
            analyses_list.append({
            'Ion': [ion.isotope.element, ion.isotope.number, ion.isotope.mass, ion.isotope.abundance, ion.charge_state],
            'Method': analysis.method,
            'Range': [analysis.range.start, analysis.range.end],
            'Reason': analysis.reason,
            'Color': analysis.color,
            })
        return analyses_list

    def make_analyses_from_mrfile(self, mrfile):
        with open(mrfile, 'r', encoding='utf-8') as f:
            contents = json.load(f)

        new_analyses = self._from_json(contents)

        return new_analyses

    def _from_json(self, contents):
        new_analyses = {}
        for entry in contents:
            if isinstance(entry, list):
                print(entry)
            if isinstance(entry, dict):
                element, number, mass, abundance, charge_state = entry.get('Ion')
                method_name = entry.get('Method')
                start, end = entry.get('Range')
                reason = entry.get('Reason')
                color = entry.get('Color')

                _range = Range(start, end)

                new_analyses.update({Ion(Isotope(element, number, mass, abundance), charge_state): Analysis(method_name, _range, reason, color)})

        return new_analyses


class MetadataModel(QObject):
    updated = pyqtSignal(tuple)

    def __init__(self):
        super(MetadataModel, self).__init__(None)

        self._metadata = ExperimentInfo(ID='Experiment ID',description='Description...')

    def replace_experiment_ID(self, new_experiment_ID):
        old_experiment_ID = self._metadata.ID
        self._metadata = self._metadata._replace(ID=new_experiment_ID)
        self.updated.emit(self._metadata)

        return old_experiment_ID

    def replace_experiment_description(self, new_experiment_description):
        old_experiment_description = self._metadata.description
        self._metadata = self._metadata._replace(description=new_experiment_description)
        self.updated.emit(self._metadata)

        return old_experiment_description

    def prime(self):
        self.updated.emit(self._metadata)

if __name__ == '__main__':
    unittest.main()
