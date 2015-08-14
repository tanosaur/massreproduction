import unittest
import numpy as np

from PyQt4.QtGui import QUndoCommand, QUndoView


class CommandAddIonsToTable(QUndoCommand):
    def __init__(self,ion_names,dataset):

        super(CommandAddIonsToTable, self).__init__('Add {0}'.format(','.join(ion_names)))
        self.ion_names=ion_names
        self.dataset=dataset

    def redo(self):
        self._original_ions_in_table=list(self.dataset.ionsintable)
        self.dataset.set_ionsintable(self.ion_names)
        self.dataset.range_table_updated.emit(self.dataset.ionsintable)

    def undo(self):
        self.dataset.ionsintable=self._original_ions_in_table
        self.dataset.range_table_updated.emit(self.dataset.ionsintable)


class CommandRemoveIonsFromTree(QUndoCommand):
    pass

class CommandSuggest(QUndoCommand):

    def __init__(self, knownelemstring, maxcsint, dataset):
        super(CommandSuggest, self).__init__('Suggest {0} ({1})'.format(knownelemstring,maxcsint))
        self.knownelemstring=knownelemstring
        self.maxcs=maxcsint
        self.dataset=dataset
        self._original_names=None
        self._original_maxcs=None
        self._original_allnames=None
        self._original_suggestedelements=None

    def redo(self):
        self._original_m2cs=np.copy(self.dataset.m2cs)
        self._original_names=np.copy(self.dataset.names)
        self._original_allnames=np.copy(self.dataset.allnames)
        # self._original_suggestedelements=list(self.dataset.suggestedelements)
        self.dataset.load_suggest(self.knownelemstring,self.maxcs)
        self.dataset.suggest.emit(self.dataset.m2cs, self.dataset.names)
        self.dataset.ion_list_updated.emit(self.dataset.allnames, self.dataset.suggestedelements)


    def undo(self):
        self.dataset.m2cs=np.copy(self._original_m2cs)
        self.dataset.names=np.copy(self._original_names)
        self.dataset.allnames=np.copy(self._original_allnames)
        # self.dataset.suggestedelements=self._original.suggestedelements
        self.dataset.suggest.emit(self.dataset.m2cs, self.dataset.names)
        self.dataset.ion_list_updated.emit(self.dataset.allnames, self.dataset.suggestedelements)

class CommandLoad(QUndoCommand):

    def __init__(self, filenames, knownelemstring, maxchargestate, method, dataset):
        super(CommandLoad, self).__init__('Load (%s)' %filenames)

        self.data=data
        self.meth=method
        self.maxcs=maxchargestate
        self.knownelemstring=knownelemstring
        self.dataset=dataset

        self._original_m2c = None

    def redo(self):
        self._original_m2c=list(self.dataset.m2c)
        self.dataset.load(self.data,self.meth,self.knownelemstring,self.maxcs)
        self.dataset.m2c_updated.emit(self.dataset.m2c)

        #self.dataset.method.rangefunction(self.dataset.m2c) #somethinglikethis

        if self.dataset.method==1:
            pass
            #place auto ranges over plot
            #place known elements and their range into table

        elif self.dataset.method==2:
            pass
            #perform an auto range method
            #place auto ranges over plot
            #place known elements and their range into table

        elif self.dataset.method==3:
            # print(type(self.dataset.knownelems))
            # print(self.dataset.knownelems[0])
            self.dataset.suggest.emit(self.dataset.knownelems, self.dataset.maxchargestate)
            #place known elements as suggest over plot

            #TODO why is this a QStringList object when in DataSet it is a list?


    def undo(self):
        self.dataset.m2c=np.asarray(self._original_m2c)
        self.dataset.m2c_updated.emit(self.dataset.m2c)
