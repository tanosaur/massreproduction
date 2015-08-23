import unittest
import numpy as np

from collections import namedtuple
from PyQt4.QtCore import QObject, pyqtSignal

class m2cModel(QObject):
    m2c_updated = pyqtSignal(list)

    def __init__(self, parent=None):
        super(m2cModel, self).__init__(parent)

        self.m2cs=[]

    def replace_m2cs(self, new_m2cs):
        old_m2cs = self.m2cs
        self.m2cs = new_m2cs

        self.m2c_updated.emit(self.m2cs)

        return old_m2cs

    def connect_signals_to_slots(self,*args):
        for view_action in args:
            self.m2c_updated.connect(view_action)


class SuggestModel(QObject):
    suggest_updated = pyqtSignal(dict)
    # Ions = namedtuple('Ions', 'name m2c abundance')
    # ions = Ions(
    #     maximum = 9000,
    #     default = 1000,
    #     minimum = 0
    # )


    def __init__(self, parent=None):
        super(SuggestModel, self).__init__(parent)

        self.known_elements=[]
        self.max_charge_state=[]

    def replace(self, new_known_elements, new_max_charge_state):
        old_known_elements = self.known_elements
        old_max_charge_state = self.max_charge_state
        self.known_elements = new_known_elements
        self.max_charge_state = new_max_charge_state

        suggested_ions=self.suggest_ions(new_known_elements, new_max_charge_state)
        self.suggest_updated.emit(suggested_ions)

        return old_known_elements, old_max_charge_state

    def suggest_ions(self, known_elements, max_charge_state):

        _lookup={
            "Al": [(27,26.98,100)], # Isotope name, mass-to-charge (Da), abundance (%)
            "Cr": [(50,49.95,4.3),(52,51.94,83.8),(53,52.94,9.5),(54,53.94,2.4)],
            "H":  [(1,1.008,99.985),(2,2.014,0.015)]
        }

        suggested_ions={}

        if known_elements or max_charge_state:
            known_elements=known_elements.split(',') #TODO guide user (grey default) # Make iterable
            for element in known_elements: # For each known element entered
                records=_lookup[element] # Get data for element from dictionary
                entries=[]
                for k in np.arange(max_charge_state)+1: # For every charge state up to the maximum charge state entered
                    for j in range(len(records)): # Store suggested ions for each isotope
                        entry=(str(records[j][0])+element+'+'+str(k), records[j][1]/k, records[j][2]) # ('27Al1+', 26.98, 100))
                        entries.append(entry)

                suggested_ions[element]=(entries)

        return suggested_ions

    def connect_signals_to_slots(self,*args):
        for view_action in args:
            self.suggest_updated.connect(view_action)


class BinSizeModel(QObject):
    bin_size_updated = pyqtSignal(int)
    Constraints = namedtuple('Constraints', 'maximum default minimum')
    constraints = Constraints(
        maximum = 9000,
        default = 1000,
        minimum = 0
    )

    def __init__(self, parent=None):
        super(BinSizeModel, self).__init__(parent)

        self.bin_size=None

    def replace_bin_size(self, new_bin_size):
        old_bin_size = self.bin_size
        self.bin_size = new_bin_size

        self.bin_size_updated.emit(self.bin_size)

        return old_bin_size

    def connect_signals_to_slots(self,*args):
        for view_action in args:
            self.bin_size_updated.connect(view_action)

class aRangeTableModel(QObject):
    range_table_updated = pyqtSignal(list)

    def __init__(self, parent=None):
        super(aRangeTableModel, self).__init__(parent)

        self.names=[]

    def update_ions(self, added_ions):
        existing_names = self.names
        self.names.append(added_ions)

        self.range_table_updated.emit(self.names)

        return existing_names

    def connect_signals_to_slots(self,*args):
        for view_action in args:
            self.range_table_updated.connect(view_action)


class TestDataSet(unittest.TestCase):

    def dataset_with_data(self):
        d = m2cModel()
        d.load(np.array([1, 2]), 2)
        return d

    def test_empty_dataset(self):
        d = m2cModel()
        self.assertTrue(np.array_equal(d.m2c, np.array([])))

    def test_load(self):
        d = self.dataset_with_data()
        self.assertTrue(np.array_equal(d.m2c, np.array([1,2])))

    def test_undo_on_empty_dataset(self):
        # Arrange
        d = m2cModel()
        d.undo() # Act
        self.assertTrue(np.array_equal(d.m2c, np.array([]))) # Assert

    def test_undo_on_changed_m2cModel(self):
        d=m2cModel()
        theonebeforechanged=d.m2c
        d.load(np.array([1, 2]), 2)
        d.undo() # Act
        self.assertTrue(np.array_equal(d.m2c,theonebeforechanged)) # Assert

    def test_redo_on_full_dataset(self):
        pass

    def test_redo_on_changed_dataset(self):
        d = self.dataset_with_data()
        original_d = d.m2c
        d.undo()
        d.redo()
        self.assertTrue(np.array_equal(d.m2c, original_d))

    def test_undo_emits_m2c_updated_signal(self):
        d = m2cModel()
        d.load(np.array([1, 2]), 2)
        self.m2c_update = False
        def _on_m2c_updated(m2c):
            self.m2c_update = m2c
        d.m2c_updated.connect(_on_m2c_updated)
        d.undo()
        self.assertTrue(np.array_equal(self.m2c_update, d.m2c))

#    def test_undo_emits_m2c_updated_signal(self):
#        d = m2cModel()
#        d.load(np.array([1, 2]), 2)
#        updated = (False, True).__iter__()
#        d.m2c_updated.connect(updated.__next__)
#        d.undo()
#        self.assertTrue(updated.__next__())



if __name__ == '__main__':
    # unittest.main()
    make=m2cModel()
    make.load(np.array([]), 2, 1, 'Al,Cr', 3)
