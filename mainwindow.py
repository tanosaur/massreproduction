from PyQt4.QtCore import pyqtSlot
from PyQt4 import QtCore
from PyQt4.QtGui import QMainWindow, QUndoStack, QUndoView, QApplication, QFileDialog, QStandardItemModel, QStandardItem
import sys
import ui_mainwindow
from plots import WorkingFrame, RangedFrame
import commands
import models
import itertools

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):

    def __init__(self, loaded_m2c_model, bin_size_model, suggested_ions_model, all_ranges_model, analyses_model, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._loaded_m2c_model = loaded_m2c_model
        self._bin_size_model = bin_size_model
        self._suggested_ions_model = suggested_ions_model
        self._all_ranges_model = all_ranges_model
        self._analyses_model = analyses_model

        self.undoStack = QUndoStack(self)
        history_view = QUndoView(self.undoStack, parent=self.stackView)
        history_view.setEmptyLabel('New program')
        self.suggestmodel=None

    @pyqtSlot(models.BinSizeRecord)
    def on_bin_size_updated(self, bin_size):
        self.binsizeSpinBox.setMaximum(bin_size.maximum)
        self.binsizeSpinBox.setMinimum(bin_size.minimum)
        self.binsizeSpinBox.setValue(bin_size.value)
        print('bin size updated')

    @pyqtSlot()
    def on_actionLoad_triggered(self):
        pos_filename=QFileDialog.getOpenFileName(self,"Open .pos file",'', 'POS (*.pos)')
        if pos_filename:
            command = commands.LoadM2C(pos_filename, self._loaded_m2c_model)
            self.undoStack.push(command)

    @pyqtSlot(int)
    def on_binsizeSpinBox_valueChanged(self, bin_size_value):
        command = commands.BinSizeValueChange(bin_size_value, self._bin_size_model)
        self.undoStack.push(command)

    @pyqtSlot()
    def on_suggestButton_clicked(self):
        command = commands.SuggestIons(
            str(self.knownelementsLineEdit.text()),
            abs(int(str(self.maxchargestateLineEdit.text()))),
            self._suggested_ions_model
        )
        self.undoStack.push(command)

    @pyqtSlot(tuple)
    def on_ions_updated(self, new_ions):

        qmodel = QStandardItemModel()
        qmodel.setColumnCount(2)
        qmodel.setHorizontalHeaderItem(0, QStandardItem('Ion'))
        qmodel.setHorizontalHeaderItem(1, QStandardItem('Abundance (%)'))

        root = qmodel.invisibleRootItem()

        element_keyfunc = lambda x: x.isotope.element
        sorted_ions = sorted(new_ions, key=element_keyfunc)

        for element, ions in itertools.groupby(sorted_ions, key=element_keyfunc):
            element_item = QStandardItem(element)
            root.appendRow(element_item)

            for ion in ions:
                ion_name = QStandardItem(ion.name)
                ion_name.setData(ion,32)
                ion_name.emitDataChanged()
                ion_abundance = QStandardItem(str(ion.isotope.abundance))
                element_item.appendRow([ion_name, ion_abundance])

        self.ionlistTree.setModel(qmodel)
        self.ionlistTree.setSelectionMode(3)
        self.ionlistTree.expandAll()
        self.ionlistTree.setSortingEnabled(True)
        self.addionsButton.setEnabled(True)
        self.suggestmodel=qmodel

    @pyqtSlot()
    def on_addionsButton_clicked(self):
        qmodel_indices=self.ionlistTree.selectedIndexes()
        ions=[self.suggestmodel.data(index,32) for index in qmodel_indices]
        command = commands.AddIonsToTable(ions, self._all_ranges_model)
        self.undoStack.push(command)

    @pyqtSlot()
    def on_analyses_updated(self):

    @pyqtSlot()
    def on_action_ExportAsMR_triggered(self):
        command = commands.ExportAnalyses(self._analyses_model)
        self.undoStack.push(command)

    @pyqtSlot()
    def on_action_LoadMR_triggered(self):
        mr_filename=QFileDialog.getOpenFileName(self,"Open .mr file",'', 'MR (*.mr)')
        if mr_filename:
            command = commands.LoadAnalyses(mr_filename, self._analyses_model)
            self.undoStack.push(command)

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self.undoStack.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self.undoStack.redo()

    @pyqtSlot(str)
    def on_maxchargestateLineEdit_textEdited(self):
        self.suggestButton.setEnabled(True)
        self.suggestButton.setFocus()

if __name__ == '__main__':
    app=QApplication(sys.argv)

    loaded_m2c_model = models.LoadedM2CModel()
    bin_size_model = models.BinSizeModel()
    suggested_ions_model = models.SuggestedIonsModel()
    all_ranges_model = models.AllRangesModel()
    committed_ranges_model = models.CommittedRangesModel()
    analyses_model = models.AnalysesModel()

    main_window = MainWindow(loaded_m2c_model, bin_size_model, suggested_ions_model, all_ranges_model, analyses_model)
    working_frame = WorkingFrame(parent=main_window.workingFrame)
    ranged_frame = RangedFrame(parent=main_window.rangedFrame)

    working_plot_view_model = models.WorkingPlotViewModel()
    final_plot_view_model = models.FinalPlotViewModel()
    analyses_table_view_model = models.AnalysesTableViewModel()

    working_plot_view_model.updated.connect(working_frame.on_updated)
    final_plot_view_model.updated.connect(ranged_frame.on_updated)
    loaded_m2c_model.updated.connect(working_plot_view_model.on_m2c_updated)
    loaded_m2c_model.updated.connect(final_plot_view_model.on_m2c_updated)

    bin_size_model.updated.connect(main_window.on_bin_size_updated)
    bin_size_model.updated.connect(working_plot_view_model.on_bin_size_updated)
    bin_size_model.updated.connect(final_plot_view_model.on_bin_size_updated)

    all_ranges_model.updated.connect(working_plot_view_model.on_ranges_updated)
    all_ranges_model.updated.connect(committed_ranges_model.on_ranges_updated)
    all_ranges_model.updated.connect(analyses_model.on_ranges_updated)

    committed_ranges_model.updated.connect(final_plot_view_model.on_ranges_updated)

    suggested_ions_model.updated.connect(working_plot_view_model.on_ions_updated)
    suggested_ions_model.updated.connect(main_window.on_ions_updated)

    analyses_model.updated.connect(analyses_table_view_model.on_analyses_updated)

    loaded_m2c_model.prime()
    bin_size_model.prime()

    main_window.show()
    app.exec_()
