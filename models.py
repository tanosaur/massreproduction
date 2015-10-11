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
    Isotope('He', 4, 4.00, 99.9999),
    Isotope('Li', 6, 6.02, 7.5),
    Isotope('Li', 7, 7.02, 92.5),
    Isotope('Be', 9, 9.01, 100),
    Isotope('B', 10, 10.01, 19.9),
    Isotope('B', 11, 11.01, 80.1),
    Isotope('C', 12, 12.00, 98.89),
    Isotope('C', 13, 13.00, 1.11),
    Isotope('N', 14, 14.00, 99.634),
    Isotope('N', 15, 15.00, 0.366),
    Isotope('O', 16, 15.995, 99.762),
    Isotope('O', 17, 17.00, 0.038),
    Isotope('O', 18, 18.00, 0.2),
    Isotope('F', 19, 19.00, 100),
    Isotope('Ne', 20, 19.99, 90.48),
    Isotope('Ne', 21, 20.99, 0.27),
    Isotope('Ne', 22, 21.99, 9.25),
    Isotope('Na', 23, 22.99, 100),
    Isotope('Mg', 24, 23.99, 78.99),
    Isotope('Mg', 25, 24.99, 10),
    Isotope('Mg', 26, 25.98, 11.01),
    Isotope('Al', 27, 26.98, 100),
    Isotope('Si', 28, 27.98, 92.23),
    Isotope('Si', 29, 28.98, 4.67),
    Isotope('Si', 30, 29.97, 3.1),
    Isotope('P', 31, 30.97, 100),
    Isotope('S', 32, 31.97, 95.02),
    Isotope('S', 33, 32.97, 0.75),
    Isotope('S', 34, 33.97, 4.21),
    Isotope('S', 36, 35.97, 0.02),
    Isotope('Cl', 35, 34.97, 75.77),
    Isotope('Cl', 37, 36.97, 24.23),
    Isotope('Ar', 36, 36.97, 0.34),
    Isotope('Ar', 38, 37.96, 0.06),
    Isotope('Ar', 40, 39.96, 99.60),
    Isotope('K', 39, 38.96, 93.258),
    Isotope('K', 40, 39.96, 0.0117),
    Isotope('K', 41, 40.96, 6.73),
    Isotope('Ca', 40, 39.96, 96.941),
    Isotope('Ca', 42, 41.96, 0.647),
    Isotope('Ca', 43, 42.96, 0.135),
    Isotope('Ca', 44, 43.96, 2.086),
    Isotope('Ca', 46, 45.95, 0.004),
    Isotope('Sc', 45, 44.96, 100),
    Isotope('Ti', 46, 45.95, 8.25),
    Isotope('Ti', 47, 46.95, 7.44),
    Isotope('Ti', 48, 47.95, 73.72),
    Isotope('Ti', 49, 48.95, 5.41),
    Isotope('Ti', 50, 49.95, 5.18),
    Isotope('V', 50, 49.95, 0.25),
    Isotope('V', 51, 50.94, 99.75),
    Isotope('Cr', 50, 49.95, 4.345),
    Isotope('Cr', 52, 51.94, 83.789),
    Isotope('Cr', 53, 52.94, 9.501),
    Isotope('Cr', 54, 53.94, 2.365),
    Isotope('Mn', 55, 54.94, 100),
    Isotope('Fe', 54, 53.94, 5.845),
    Isotope('Fe', 56, 55.94, 91.754),
    Isotope('Fe', 57, 56.94, 2.119),
    Isotope('Fe', 58, 57.93, 0.282),
    Isotope('Co', 59, 58.93, 100),
    Isotope('Ni', 58, 57.94, 68.077),
    Isotope('Ni', 60, 59.93, 26.223),
    Isotope('Ni', 61, 60.93, 1.14),
    Isotope('Ni', 62, 61.93, 3.634),
    Isotope('Ni', 64, 63.93, 0.926),
    Isotope('Cu', 63, 62.93, 69.17),
    Isotope('Cu', 65, 64.93, 30.83),
    Isotope('Zn', 64, 63.93, 48.6),
    Isotope('Zn', 66, 65.93, 27.9),
    Isotope('Zn', 67, 66.93, 4.1),
    Isotope('Zn', 68, 67.93, 18.8),
    Isotope('Zn', 70, 69.93, 0.6),
    Isotope('Ga', 69, 68.93, 60.108),
    Isotope('Ga', 71, 70.93, 39.892),
    Isotope('Ge', 70, 69.92, 21.23),
    Isotope('Ge', 72, 71.92, 27.66),
    Isotope('Ge', 73, 72.92, 7.73),
    Isotope('Ge', 74, 73.92, 35.94),
    Isotope('Ge', 76, 75.92, 7.44),
    Isotope('As', 75, 74.92, 100),
    Isotope('Se', 74, 73.92, 0.89),
    Isotope('Se', 76, 75.92, 9.36),
    Isotope('Se', 77, 76.92, 7.63),
    Isotope('Se', 78, 77.92, 23.78),
    Isotope('Se', 80, 79.92, 49.61),
    Isotope('Se', 82, 81.92, 8.73),
    Isotope('Br', 79, 78.92, 50.69),
    Isotope('Br', 81, 80.92, 49.31),
    Isotope('Kr', 79, 78.92, 0.35),
    Isotope('Kr', 80, 79.92, 2.25),
    Isotope('Kr', 82, 81.91, 11.6),
    Isotope('Kr', 83, 82.91, 11.5),
    Isotope('Kr', 84, 83.91, 57),
    Isotope('Kr', 86, 85.91, 17.3),
    Isotope('Rb', 85, 84.91, 72.165),
    Isotope('Rb', 87, 86.91, 27.835),
    Isotope('Sr', 84, 83.91, 0.56),
    Isotope('Sr', 86, 85.91, 9.86),
    Isotope('Sr', 87, 86.91, 7.02),
    Isotope('Sr', 88, 87.91, 82.58),
    Isotope('Y', 89, 88.91, 100),
    Isotope('Zr', 90, 89.91, 51.45),
    Isotope('Zr', 91, 90.91, 11.22),
    Isotope('Zr', 92, 91.91, 17.15),
    Isotope('Zr', 94, 93.91, 17.38),
    Isotope('Zr', 96, 95.91, 2.8),
    Isotope('Nb', 93, 92.91, 100),
    Isotope('Mo', 92, 91.91, 14.84),
    Isotope('Mo', 94, 93.91, 9.25),
    Isotope('Mo', 95, 94.91, 15.92),
    Isotope('Mo', 96, 95.91, 16.68),
    Isotope('Mo', 97, 96.91, 9.55),
    Isotope('Mo', 98, 97.91, 24.13),
    Isotope('Mo', 100, 99.91, 9.63),
    Isotope('Ru', 96, 95.91, 5.52),
    Isotope('Ru', 98, 97.91, 1.88),
    Isotope('Ru', 99, 98.91, 12.7),
    Isotope('Ru', 100, 99.90, 12.6),
    Isotope('Ru', 101, 100.91, 17),
    Isotope('Ru', 102, 101.90, 31.6),
    Isotope('Ru', 104, 103.91, 18.7),
    Isotope('Rh', 103, 102.91, 100),
    Isotope('Pd', 102, 101.91, 1.02),
    Isotope('Pd', 104, 103.90, 11.14),
    Isotope('Pd', 105, 104.91, 22.33),
    Isotope('Pd', 106, 105.90, 27.33),
    Isotope('Pd', 108, 107.90, 26.46),
    Isotope('Pd', 110, 109.91, 11.72),
    Isotope('Ag', 107, 106.91, 51.839),
    Isotope('Ag', 109, 108.91, 48.161),
    Isotope('Cd', 106, 105.91, 1.25),
    Isotope('Cd', 108, 107.90, 0.89),
    Isotope('Cd', 110, 109.90, 12.49),
    Isotope('Cd', 111, 110.90, 12.8),
    Isotope('Cd', 112, 111.90, 24.13),
    Isotope('Cd', 113, 112.90, 12.22),
    Isotope('Cd', 114, 113.90, 28.73),
    Isotope('Cd', 116, 115.90, 7.49),
    Isotope('In', 113, 112.90, 4.29),
    Isotope('In', 115, 114.90, 95.71),
    Isotope('Sn', 112, 111.90, 0.97),
    Isotope('Sn', 114, 113.90, 0.65),
    Isotope('Sn', 115, 114.90, 0.34),
    Isotope('Sn', 116, 115.90, 14.54),
    Isotope('Sn', 117, 116.90, 7.68),
    Isotope('Sn', 118, 117.90, 24.22),
    Isotope('Sn', 119, 118.90, 8.58),
    Isotope('Sn', 120, 119.90, 32.59),
    Isotope('Sn', 122, 121.90, 4.63),
    Isotope('Sn', 124, 123.91, 5.79),
    Isotope('Sb', 121, 120.90, 57.21),
    Isotope('Sb', 123, 122.90, 42.79),
    Isotope('Te', 120, 119.90, 0.096),
    Isotope('Te', 122, 121.90, 2.603),
    Isotope('Te', 123, 122.90, 0.908),
    Isotope('Te', 124, 123.90, 4.816),
    Isotope('Te', 125, 124.90, 7.139),
    Isotope('Te', 126, 125.90, 18.952),
    Isotope('Te', 128, 127.90, 31.687),
    Isotope('Te', 130, 129.91, 33.799),
    Isotope('I', 127, 126.90, 100),
    Isotope('Xe', 124, 123.91, 0.1),
    Isotope('Xe', 126, 125.90, 0.09),
    Isotope('Xe', 128, 127.90, 1.91),
    Isotope('Xe', 129, 128.90, 26.4),
    Isotope('Xe', 130, 129.90, 4.1),
    Isotope('Xe', 131, 130.91, 21.2),
    Isotope('Xe', 132, 131.90, 26.9),
    Isotope('Xe', 134, 133.91, 10.4),
    Isotope('Xe', 136, 135.91, 8.9),
    Isotope('Cs', 133, 132.91, 100),
    Isotope('Ba', 130, 129.91, 0.106),
    Isotope('Ba', 132, 131.91, 0.101),
    Isotope('Ba', 134, 133.90, 2.417),
    Isotope('Ba', 135, 134.90, 6.592),
    Isotope('Ba', 136, 135.90, 7.854),
    Isotope('Ba', 137, 136.91, 11.23),
    Isotope('Ba', 138, 137.91, 71.7),
    Isotope('Ce', 136, 135.91, 0.19),
    Isotope('Ce', 138, 137.91, 0.25),
    Isotope('Ce', 140, 139.91, 88.48),
    Isotope('Ce', 142, 141.91, 11.08),
    Isotope('Pr', 141, 140.91, 100),
    Isotope('Nd', 142, 141.91, 27.13),
    Isotope('Nd', 143, 142.91, 12.18),
    Isotope('Nd', 144, 143.91, 23.8),
    Isotope('Nd', 145, 144.91, 8.3),
    Isotope('Nd', 146, 145.91, 17.19),
    Isotope('Nd', 148, 147.92, 5.76),
    Isotope('Nd', 150, 149.92, 5.64),
    Isotope('Hf', 174, 173.94, 0.162),
    Isotope('Hf', 176, 175.94, 5.206),
    Isotope('Hf', 177, 176.94, 18.606),
    Isotope('Hf', 178, 177.94, 27.297),
    Isotope('Hf', 179, 178.95, 13.629),
    Isotope('Hf', 180, 179.95, 35.1),
    Isotope('Ta', 180, 179.95, 0.012),
    Isotope('Ta', 181, 180.95, 99.988),
    Isotope('W', 180, 179.95, 0.12),
    Isotope('W', 182, 181.95, 26.498),
    Isotope('W', 183, 182.95, 14.314),
    Isotope('W', 184, 183.95, 30.642),
    Isotope('W', 186, 185.95, 28.426),
    Isotope('Re', 185, 184.95, 37.4),
    Isotope('Re', 187, 186.96, 62.6),
    Isotope('Os', 184, 183.95, 0.02),
    Isotope('Os', 186, 185.95, 1.58),
    Isotope('Os', 187, 186.96, 1.6),
    Isotope('Os', 188, 187.96, 13.3),
    Isotope('Os', 189, 188.96, 16.1),
    Isotope('Os', 190, 189.96, 26.4),
    Isotope('Os', 192, 191.96, 41),
    Isotope('Ir', 191, 190.96, 37.3),
    Isotope('Ir', 193, 192.96, 63.7),
    Isotope('Pt', 190, 189.96, 0.01),
    Isotope('Pt', 192, 191.96, 0.79),
    Isotope('Pt', 194, 193.96, 32.9),
    Isotope('Pt', 195, 194.96, 33.8),
    Isotope('Pt', 196, 195.96, 25.3),
    Isotope('Pt', 198, 197.97, 7.2),
    Isotope('Au', 197, 196.97, 100),
    Isotope('Hg', 196, 195.97, 0.15),
    Isotope('Hg', 198, 197.97, 9.97),
    Isotope('Hg', 199, 198.97, 16.87),
    Isotope('Hg', 200, 199.97, 23.1),
    Isotope('Hg', 201, 200.97, 13.18),
    Isotope('Hg', 202, 201.97, 29.86),
    Isotope('Hg', 204, 203.97, 6.87),
    Isotope('Pb', 204, 203.97, 1.4),
    Isotope('Pb', 206, 205.97, 24.1),
    Isotope('Pb', 207, 206.98, 22.1),
    Isotope('Pb', 208, 207.98, 52.4),
    Isotope('Bi', 209, 208.98, 100),
    Isotope('Th', 232, 232.04, 100),
    Isotope('U', 234, 234.04, 5.50E-03),
    Isotope('U', 235, 235.04, 0.72),
    Isotope('U', 238, 238.05, 99.27),
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

    def delete_analyses(self, ions_to_delete):
        old_analyses = self._analyses.copy()

        for ion in ions_to_delete:
            self._analyses.pop(ion)

        self.updated.emit(self._analyses)

        return old_analyses

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
