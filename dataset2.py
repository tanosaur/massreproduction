import unittest
import numpy as np
from PyQt4.QtCore import QObject, pyqtSignal

class DataSet(QObject):
    m2c_updated = pyqtSignal(np.ndarray)
    suggest=pyqtSignal(list)

    def __init__(self, parent=None):
        super(DataSet, self).__init__(parent)
        self.m2c=np.array([])
        self.method=-1
        self.maxchargestate=0
        self.knownelems=np.array([])
        self.suggestions=[]

        #Thinking that charge states will be implemented as next row (isotopes with same charge state on same row)
        #TODO investigate charge states vs. Peter's code

    def load(self, data, method, knownelemstring, maxchargestate):
        self.m2c=np.append(self.m2c,data)
        self.method=method
        self.maxchargestate=abs(maxchargestate)
        knownelemstring=str(knownelemstring) #TODO WHY WAS THIS NECESSARY
        self.knownelems=knownelemstring.split(',')
        # print(knownelemstring)
        # print(type(knownelemstring))
        # print(self.knownelems)
        # Convert string to individual element in array
        # print(self.knownelems[0]) #To access each element of string

    def load_suggest(self,suggestelemstring,maxchargestate):
        suggestedelements=suggestelemstring.split(',')
        for element in suggestedelements:
            self.suggestions.append((element, maxchargestate))

class TestDataSet(unittest.TestCase):

    def dataset_with_data(self):
        d = DataSet()
        d.load(np.array([1, 2]), 2)
        return d

    def test_empty_dataset(self):
        d = DataSet()
        self.assertTrue(np.array_equal(d.m2c, np.array([])))

    def test_load(self):
        d = self.dataset_with_data()
        self.assertTrue(np.array_equal(d.m2c, np.array([1,2])))

    def test_undo_on_empty_dataset(self):
        # Arrange
        d = DataSet()
        d.undo() # Act
        self.assertTrue(np.array_equal(d.m2c, np.array([]))) # Assert

    def test_undo_on_changed_dataset(self):
        d=DataSet()
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
        d = DataSet()
        d.load(np.array([1, 2]), 2)
        self.m2c_update = False
        def _on_m2c_updated(m2c):
            self.m2c_update = m2c
        d.m2c_updated.connect(_on_m2c_updated)
        d.undo()
        self.assertTrue(np.array_equal(self.m2c_update, d.m2c))

#    def test_undo_emits_m2c_updated_signal(self):
#        d = DataSet()
#        d.load(np.array([1, 2]), 2)
#        updated = (False, True).__iter__()
#        d.m2c_updated.connect(updated.__next__)
#        d.undo()
#        self.assertTrue(updated.__next__())

if __name__ == '__main__':
    # unittest.main()
    make=DataSet()
    make.load(np.array([]), 2, 1, 'Al,Cr', 3)
