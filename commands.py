import unittest
import numpy as np

from PyQt4.QtGui import QUndoCommand, QUndoView

class StackView(QUndoView):

    def __init__(self, undostack, parent):
        super(StackView, self).__init__(parent)

class CommandSuggest(QUndoCommand):

    def __init__(self, description, dataset):
        super(CommandSuggest, self).__init__(description)

        self.dataset=dataset
        self.elemhistory=[]
        self.maxcshistory=[]
        self.elemfuture=[]
        self.maxcsfuture=[]

    def redo(self):
        self.dataset.suggest.emit(self.dataset.suggestelems,self.dataset.suggestmcs)
        self.elemhistory.append(self.dataset.suggestelems)
        self.maxcshistory.append(self.dataset.suggestmcs)

    def undo(self):
        self.elemfuture.append(self.elemhistory.pop()) #TODO check with Scott
        self.maxcsfuture.append(self.maxcshistory.pop())
        #
        # if self.elemhistory!=[]: #TODO make sure both fields are entered compulsory in view
        #     self.dataset.suggestelems=self.elemhistory.pop()
        #     self.dataset.suggestmcs=self.maxcshistory.pop()
        # else:
        #     self.dataset.suggestelems=[]
        #     self.dataset.suggestmcs=0
        #
        # self.dataset.suggest.emit(self.dataset.suggestelems,self.dataset.suggestmcs)
        self.dataset.suggestUndo.emit()

class CommandLoad(QUndoCommand):
    #TODO where to put all this and pyqtSignal

    def __init__(self, data, method, knownelemstring, maxchargestate, description, dataset):
        super(CommandLoad, self).__init__(description)

        self.data=data
        self.meth=method
        self.maxcs=maxchargestate
        self.knownelemstring=knownelemstring
        self.dataset=dataset #TODO Ask Scott

        # Had to do this because redo and undo could only take in 1 argument, self.
        self.history=[]

    def redo(self):
        self.dataset.load(self.data,self.meth,self.knownelemstring,self.maxcs)
        self.history.append(self.dataset.m2c)
        self.dataset.m2c_updated.emit(self.dataset.m2c)

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
        self.history.pop() #TODO check with Scott
        if self.history!=[]:
            self.dataset.m2c=self.history.pop()
        else:
            self.dataset.m2c=np.array([])
        self.dataset.m2c_updated.emit(self.dataset.m2c)
