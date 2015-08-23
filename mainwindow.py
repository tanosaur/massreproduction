from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4.QtGui import *
import sys

import ui_mainwindow
import ui_historywidget #TODO implement

from plots import WorkingFrame, RangedFrame
from commands import *
from dataset import m2cModel, SuggestModel, BinSizeModel, aRangeTableModel
from nodetrees import Node, IonListModel, Node2, RangeTableModel
import numpy as np #TODO get rid of when not needed anymore

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Call setupUi to instantiate as in .ui (see ui_mainwindow.py)
        self.setupUi(self)

        # INSTANCES
        self.m2c_model = m2cModel(self)
        self.suggest_model = SuggestModel(self)
        self.bin_size_model = BinSizeModel(self)
        self.range_table_model = aRangeTableModel(self)

        self.undoStack = QUndoStack(self)
        self.history_view = QUndoView(self.undoStack, parent=self.stackView)
        self.history_view.setEmptyLabel('New program')

        self.working_frame=WorkingFrame(parent=self.workingFrame)
        self.ranged_frame=RangedFrame(parent=self.rangedFrame)

        # SIGNAL/SLOT CONNECTS
        self.suggest_model.connect_signals_to_slots(self.working_frame.on_suggest_updated, self.on_suggest_updated)
        self.m2c_model.connect_signals_to_slots(self.working_frame.on_m2c_updated)
        self.bin_size_model.connect_signals_to_slots(self.working_frame.on_bin_size_updated)
        self.range_table_model.connect_signals_to_slots(self.on_range_table_updated)

        # DEFAULTS
        self.binsizeSpinBox.setMaximum(BinSizeModel.constraints.maximum)
        self.binsizeSpinBox.setMinimum(BinSizeModel.constraints.minimum)
        self.binsizeSpinBox.setValue(BinSizeModel.constraints.default)

        ion_list_root=Node('IonList')
        ion_list=IonListModel(ion_list_root)
        self.ionlistTree.setModel(ion_list)

        self.range_table_root=Node2('RangeList', '', '', '')
        self.range_table=RangeTableModel(self.range_table_root)
        self.rangedTable.setModel(self.range_table)

    @pyqtSignature("") # Must be included even if ""
    def on_actionLoad_triggered(self):
        pos_filename=QFileDialog.getOpenFileName(self,"Open .pos file",'', 'POS (*.pos)')
        commandLoadData=CommandLoadData(pos_filename, self.m2c_model)
        self.undoStack.push(commandLoadData) #Calls the 'redo' method
        #     #see https://forum.qt.io/topic/12330/qundocommand-calls-redo-on-initialization/6

    @pyqtSlot(int)
    def on_binsizeSpinBox_valueChanged(self, bin_size):
        commandBinSizeChange=CommandBinSizeChange(bin_size, self.bin_size_model, self.m2c_model)
        self.undoStack.push(commandBinSizeChange)

    @pyqtSignature("")
    def on_suggestButton_clicked(self):
        commandSuggest=CommandSuggest(
            str(self.knownelementsLineEdit.text()),
            abs(int(str(self.maxchargestateLineEdit.text()))),
            self.suggest_model
        )
        self.undoStack.push(commandSuggest)

    @pyqtSlot(dict)
    def on_suggest_updated(self, suggested_ions):
        ion_list_root=Node('IonList')

        for element, ions in suggested_ions.items():
            element_node=Node(element, ion_list_root)
            for ion in ions:
                label, m2c, abundance = ion
                Node(label,element_node,str(abundance))

        ion_list=IonListModel(ion_list_root)
        self.ionlistTree.setModel(ion_list)

        self.ionlistTree.setSelectionMode(3)
        self.ionlistTree.expandAll()
        self.ionlistTree.setSortingEnabled(True)
        self.ionlistTree.sortByColumn(1, 0) # TODO not working, set first column spanned?

    @pyqtSignature("")
    def on_addionsButton_clicked(self):
        qmodel_indices=self.ionlistTree.selectedIndexes() # Retrieve highlighted labels

        # ions = [index.internalPointer().ion for index in qmodel_indices]
        # for ion in ions:
        #     print(ion.name)
        #     print(ion.m2c)
        #     print(ion.abundance)

        # names =[self.ion_list.data(x, role=QtCore.Qt.DisplayRole) for x in qmodel_indices]
        # commandAddIons=CommandAddIonsToTable(refs, self.range_table_model) # Add the name to the table
        # self.undoStack.push(commandAddIons)

    @pyqtSlot(list)
    def on_range_table_updated(self, ion_names):
        for line in ion_names:
            for x in line:
                Node2(x, '', '', '',self.range_table_root)

        self.rangedTable.setModel(self.range_table)


    # @pyqtSignature("") # Must be included even if ""
    # def on_actionHistory_triggered(self):
    #     histDlg=histWidget(self, self.undoStack)
    #     histDlg.setModal(True) #see how this actually affects things later
    #     histDlg.exec_() #TODO implement history view as new window or side window

    @pyqtSignature("") # Must be included even if ""
    def on_actionSave_As_triggered(self):
        print("save as triggered")

    @pyqtSignature("") # Must be included even if ""
    def on_actionSave_triggered(self):
        print("save triggered")

    @pyqtSignature("") # Must be included even if ""
    def on_actionUndo_triggered(self):
        print("undo triggered")
        self.undoStack.undo()

    @pyqtSignature("") # Must be included even if ""
    def on_actionRedo_triggered(self):
        print("redo triggered")
        self.undoStack.redo()

    def updateUi(self):
        enable=not self.knownelementsLineEdit.text().isEmpty() #TODO #add suggestLineEdit test as well
        # Enables the 'Suggest' button
        self.suggestButton.setEnabled(enable) #TODO initially disable this and also load button

    @pyqtSignature("QString")
    def on_knownelementsLineEdit_textEdited(self,text):
        self.updateUi()

app=QApplication(sys.argv)
form=MainWindow()
form.show()
# s=MainWindow.RangedFrame.size()
# MainWindow.plotWidget.setGeometry(1,1, s.width()-2, s.height()-2)
app.exec_()
