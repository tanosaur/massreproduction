import unittest
import numpy as np
from PyQt4.QtCore import QObject, pyqtSignal

class DataSet(QObject):
    m2c_updated = pyqtSignal(np.ndarray)
    suggest=pyqtSignal(np.ndarray, np.ndarray)
    ion_list_updated=pyqtSignal(np.ndarray, list)
    range_table_updated=pyqtSignal(list)

    def __init__(self, parent=None):
        super(DataSet, self).__init__(parent)
        self.m2c=[]
        self.method=None
        self.maxchargestate=None
        self.knownelems=None

        self.names=[]
        self.m2cs=[]
        self.allnames=np.array([])
        self.suggestedelements=[]

        self.ionsintable=[]

    def set_ionsintable(self,loadionlist):
        self.ionsintable.append(loadionlist)

    def load(self, data, method, knownelemstring, maxchargestate):
        self.m2c=data
        self.method=method
        self.maxchargestate=abs(maxchargestate)
        knownelemstring=str(knownelemstring) #TODO WHY WAS THIS NECESSARY
        self.knownelems=knownelemstring.split(',')

    def load_suggest(self,suggestelemstring,maxchargestate):
        self.suggestedelements=suggestelemstring.split(',')

        _lookup={
            "Al": [(27,26.98,100)],
            "Cr": [(50,49.95,4.3),(52,51.94,83.8),(53,52.94,9.5),(54,53.94,2.4)],
            "H":  [(1,1.008,99.985),(2,2.014,0.015)]
        }

        for element in self.suggestedelements:
            records=_lookup[element]
            names=np.empty(len(records)*maxchargestate,dtype=object)
            m2cs=np.empty(len(records)*maxchargestate)
            abundance=np.empty(len(records)*maxchargestate)

        #Thinking that charge states will be implemented as next row (isotopes with same charge state on same row)
        #TODO investigate charge states vs. Peter's code

            for k in np.arange(maxchargestate)+1:
                for j in np.arange(len(records)):
                    names[j+((k-1)*len(records))]=str(records[j][0])+element+'+'+str(k) #concat with element name and charge state
                    m2cs[j+((k-1)*len(records))]=records[j][1]/k
                    abundance[j+((k-1)*len(records))]=records[j][2]

        self.names=names
        self.m2cs=m2cs
        self.allnames=np.append(self.allnames, self.names)


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
