from collections import namedtuple
import unittest
import itertools
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
ExperimentInfo = namedtuple('Experiment', 'ID description')
BinSizeRecord = namedtuple('BinSizeRecord', 'maximum minimum value')

RGB = [
(41,208,208), # Cyan
(255,146,51), # Orange
(129,38,192), # Purple
(29,105,20), # Green
(255,238,51), # Yellow
(173,35,35), # Red
(42,76,215), # Blue
(87,87,87), # Dark grey
(129,74,25), # Brown
(129,197,122), # Light green
(255,205,243), # Pink
(157,175,255), # Light blue
(160,160,160), # Light grey
(233,222,187), # Tan
]

RGB = [tuple(list(val/255 for val in color)) for color in RGB]
print(RGB)

class M2CModel(QObject):
    updated = pyqtSignal(tuple)

    def __init__(self):
        super(M2CModel, self).__init__(None)

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
            minimum = 10,
            value = 2000
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

class AnalysesModel(QObject):
    updated = pyqtSignal(dict)

    def __init__(self):
        super(AnalysesModel, self).__init__(None)

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

    def update_reason_for_ion(self, ion, reason):
        old_analysis = self._analyses[ion]
        self._analyses[ion] = old_analysis._replace(
            reason=reason)
        self.updated.emit(self._analyses)

        return ion, old_analysis.reason

    def analyses_from_suggest(self, new_ions):
        new_analyses = self._color_by_element(new_ions)
        return new_analyses

    def _color_by_element(self, new_ions):
        new_analyses = {}
        existent_color_mapping = {}

        for ion in self._analyses.keys():
            existent_color_mapping.update({ion.isotope.element: self._analyses[ion].color})

        used_colors = [existent_color_mapping[element] for element in existent_color_mapping]
        unused_colors = list(set(RGB) - set(used_colors))
        colors = itertools.cycle(unused_colors)
        element_keyfunc = lambda x: x.isotope.element
        sorted_ions = sorted(new_ions, key=element_keyfunc)

        for element, ions in itertools.groupby(sorted_ions, key=element_keyfunc):

            if element in existent_color_mapping.keys():
                color = existent_color_mapping[element]
            else:
                color = next(colors)

            for ion in ions:
                new_analyses.update({ion: Analysis(method='Manual', range=Range(start=ion.mass_to_charge, end=ion.mass_to_charge), reason=None, color=color)})
                print(color)
        return new_analyses

class MetadataModel(QObject):
    updated = pyqtSignal(tuple)

    def __init__(self):
        super(MetadataModel, self).__init__(None)

        self._metadata = ExperimentInfo(ID='Experiment ID',description='Description/Notes...')

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

    def replace(self, new_metadata):
        old_metadata = self._metadata
        self._metadata = new_metadata
        self.updated.emit(self._metadata)

        return old_metadata

    def prime(self):
        self.updated.emit(self._metadata)

if __name__ == '__main__':
    unittest.main()
