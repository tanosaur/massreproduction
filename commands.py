import unittest
import numpy as np

from PyQt4.QtGui import QUndoCommand, QUndoView

# class StackView(QUndoView):
#
#     def __init__(self, undostack, parent):
#         super(StackView, self).__init__(parent)

class CommandSuggest(QUndoCommand):
    def __init__(self, knownelements, maxchargestate, dataset):
        super(CommandSuggest, self).__init__('Suggest ions')

        self.knownelements = knownelements
        self.maxchargestate = maxchargestate
        self.dataset = dataset

    def redo(self):
        self._original_suggestions = list(self.dataset.suggestions)
        self.dataset.load_suggest(self.knownelements, self.maxchargestate)
        self.dataset.suggest.emit(self.dataset.suggestions)

    def undo(self):
        self.dataset.suggestions = self._original_suggestions
        self.dataset.suggest.emit(self.dataset.suggestions)

class CommandLoad(QUndoCommand):

    def __init__(self, data, method, knownelemstring, maxchargestate, description, dataset):
        super(CommandLoad, self).__init__(description)

        self.data=data
        self.meth=method
        self.maxcs=maxchargestate
        self.knownelemstring=knownelemstring
        self.dataset=dataset #TODO Ask Scott

        # Had to do this because redo and undo could only take in 1 argument, self.
        self._original_m2c = None

    def redo(self):
        self._original_m2c = list(self.dataset.m2c) # BEFORE LOAD
        self.dataset.load(self.data,self.meth,self.knownelemstring,self.maxcs)
        self.dataset.m2c_updated.emit(self.dataset.m2c) # AFTER LOAD

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
        self.dataset.m2c = self._original_m2c
        self.dataset.m2c_updated.emit(self.dataset.m2c)
