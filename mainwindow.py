from PyQt4.QtCore import pyqtSlot, Qt, pyqtProperty, QModelIndex
from PyQt4.QtGui import QMainWindow, QUndoStack, QUndoView, QApplication, QFileDialog, QStandardItemModel, QItemSelection, QStandardItem, QComboBox, QStyledItemDelegate, QLabel, QItemSelectionModel

import sys
import ui_mainwindow
from plots import WorkingFrame, RangedFrame
import viewmodels
import commands
import models
import itertools
from methods import load_all_methods_from_dir

class MethodsComboDelegate(QStyledItemDelegate):
    def __init__(self, methods, parent):
        super(MethodsComboDelegate, self).__init__(parent)

        self._methods = methods

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        methods = list(self._methods.keys())
        combo.addItems(methods)
        combo.setCurrentIndex(methods.index(index.data()))
        return combo

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):

    def __init__(self, undo_stack, loaded_m2cs_model, bin_size_model, suggested_ions_model, analyses_model, methods_view_model, metadata_model, mr_view_model, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._undo_stack = undo_stack
        self._loaded_m2cs_model = loaded_m2cs_model
        self._bin_size_model = bin_size_model
        self._suggested_ions_model = suggested_ions_model
        self._analyses_model = analyses_model
        self._methods_model = methods_model
        self._metadata_model = metadata_model

        self._methods_view_model = methods_view_model
        self._mr_view_model = mr_view_model

        history_view = QUndoView(self._undo_stack, parent=self.stackView)
        history_view.setEmptyLabel('New program')
        self.suggestmodel=None

    @pyqtSlot(models.BinSizeRecord)
    def on_bin_size_updated(self, bin_size):
        self.binsizeSpinBox.setMaximum(bin_size.maximum)
        self.binsizeSpinBox.setMinimum(bin_size.minimum)
        self.binsizeSpinBox.setValue(bin_size.value)

    @pyqtSlot()
    def on_actionLoad_triggered(self):
        pos_filename=QFileDialog.getOpenFileName(self,"Open .pos file",'', 'POS (*.pos)')
        if pos_filename:
            command = commands.LoadPOS(pos_filename, self._loaded_m2cs_model, self._metadata_model)
            self._undo_stack.push(command)

    @pyqtSlot(int)
    def on_binsizeSpinBox_valueChanged(self, bin_size_value):
        command = commands.BinSizeValueChange(bin_size_value, self._bin_size_model)
        self._undo_stack.push(command)

    @pyqtSlot()
    def on_suggestButton_clicked(self):
        command = commands.SuggestIons(
            self.knownelementsLineEdit.text(),
            abs(int(self.maxchargestateLineEdit.text())),
            self._suggested_ions_model
        )
        self._undo_stack.push(command)

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
            element_item.setCheckable(True)
            element_item.setCheckState(2)
            root.appendRow(element_item)

            for ion in ions:
                ion_name = QStandardItem(ion.name)
                ion_name.setData(ion,32)
                ion_name.emitDataChanged()
                ion_abundance = QStandardItem(str(ion.isotope.abundance))
                element_item.appendRow([ion_name, ion_abundance])

        self.ionlistTree.setModel(qmodel)
        self.ionlistTree.expandAll()
        self.addionsButton.setEnabled(True)
        self.addionsButton.setFocus()
        self.suggestmodel=qmodel

    @pyqtSlot()
    def on_addionsButton_clicked(self):
        qmodel_indices=self.ionlistTree.selectedIndexes()
        # TODO fix so filter not needed, otherwise, leave comment explanation
        ions=list(filter(None,[self.suggestmodel.data(index,32) for index in qmodel_indices]))
        command = commands.AddIonsToTable(ions, self._analyses_model)
        self._undo_stack.push(command)

    @pyqtSlot(dict)
    def on_analyses_viewmodel_updated(self, view_model):
        qmodel = QStandardItemModel()
        qmodel.itemChanged.connect(self.on_qmodel_itemChanged)
        qmodel.setColumnCount(5)
        qmodel.setHorizontalHeaderItem(0, QStandardItem('Ion'))
        qmodel.setHorizontalHeaderItem(1, QStandardItem('Method'))
        qmodel.setHorizontalHeaderItem(2, QStandardItem('Start'))
        qmodel.setHorizontalHeaderItem(3, QStandardItem('End'))
        qmodel.setHorizontalHeaderItem(4, QStandardItem('Reason'))

        root = qmodel.invisibleRootItem()

        for ion, analysis in view_model.analyses.items():
            ion_name = QStandardItem(ion.name)
            ion_name.setData(ion, Qt.UserRole)
            method = QStandardItem(analysis.method)
            start = QStandardItem(str(round(analysis.range.start,2)))
            end = QStandardItem(str(round(analysis.range.end,2)))
            reason = QStandardItem(analysis.reason)

            root.appendRow([ion_name, method, start, end, reason])

        self.rangedTable.setModel(qmodel)
        self.rangedTable.setItemDelegateForColumn(1, MethodsComboDelegate(view_model.methods, self.rangedTable))
        for row in range(0, qmodel.rowCount()):
            self.rangedTable.openPersistentEditor(qmodel.index(row, 1))
        self.rangedTable.setColumnWidth(1, 95)

    @pyqtSlot(QStandardItem)
    def on_qmodel_itemChanged(self, item):
        index = item.index()
        ion_index = index.sibling(index.row(), 0)
        method_index = index.sibling(index.row(), 1)

        ion = ion_index.data(Qt.UserRole)
        method_name = method_index.data(Qt.DisplayRole)

        print("Change: %s : %s" % (ion, method_name))

        command = commands.MethodSelected(ion, method_name, self._analyses_model, self._methods_view_model)
        self._undo_stack.push(command)

    @pyqtSlot()
    def on_action_ExportAsMR_triggered(self):
        command = commands.ExportAnalyses(self._mr_view_model)
        self._undo_stack.push(command)

    @pyqtSlot()
    def on_action_LoadMR_triggered(self):
        mr_filename=QFileDialog.getOpenFileName(self,"Open .mr file",'', 'MR (*.mr)')
        if mr_filename:
            command = commands.LoadAnalyses(mr_filename, self._analyses_model)
            self._undo_stack.push(command)

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self._undo_stack.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self._undo_stack.redo()

    @pyqtSlot(str)
    def on_maxchargestateLineEdit_textEdited(self):
        self.suggestButton.setEnabled(True)
        self.suggestButton.setFocus()

    @pyqtSlot()
    def on_experimentIDLineEdit_editingFinished(self):
        experiment_ID = self.experimentIDLineEdit.text()
        command = commands.UpdateExperimentID(experiment_ID, metadata_model)

    @pyqtSlot()
    def on_experimentdescriptionTextEdit_textChanged(self):
        experiment_description = self.experimentdescriptionTextEdit.document().toPlainText()
        command = commands.UpdateExperimentDescription(experiment_description, metadata_model)

    @pyqtSlot(tuple)
    def on_metadata_updated(self, metadata):
        self.experimentIDLineEdit.setText(metadata.ID)
        self.experimentdescriptionTextEdit.setPlainText(metadata.description)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    print('Loading...')

    undo_stack = QUndoStack()

    loaded_m2cs_model = models.LoadedM2CModel()
    bin_size_model = models.BinSizeModel()
    suggested_ions_model = models.SuggestedIonsModel()
    committed_analyses_model = models.CommittedAnalysesModel()
    methods_model = models.MethodsModel()
    all_analyses_model = models.AllAnalysesModel()
    metadata_model = models.MetadataModel()


    working_plot_view_model = viewmodels.WorkingPlotViewModel()
    final_plot_view_model = viewmodels.FinalPlotViewModel()
    methods_view_model = viewmodels.MethodsViewModel()
    mr_view_model = viewmodels.MRViewModel()

    main_window = MainWindow(undo_stack, loaded_m2cs_model, bin_size_model, suggested_ions_model, all_analyses_model, methods_view_model, metadata_model, mr_view_model)
    working_frame = WorkingFrame(parent=main_window.workingFrame)
    ranged_frame = RangedFrame(parent=main_window.rangedFrame)

    working_plot_view_model.updated.connect(working_frame.on_updated)
    final_plot_view_model.updated.connect(ranged_frame.on_updated)
    loaded_m2cs_model.updated.connect(working_plot_view_model.on_m2cs_updated)
    loaded_m2cs_model.updated.connect(final_plot_view_model.on_m2cs_updated)
    loaded_m2cs_model.updated.connect(methods_view_model.on_methods_updated)

    bin_size_model.updated.connect(main_window.on_bin_size_updated)
    bin_size_model.updated.connect(working_plot_view_model.on_bin_size_updated)
    bin_size_model.updated.connect(final_plot_view_model.on_bin_size_updated)
    bin_size_model.updated.connect(methods_view_model.on_methods_updated)

    all_analyses_model.updated.connect(working_plot_view_model.on_all_analyses_updated)
    all_analyses_model.updated.connect(committed_analyses_model.on_all_analyses_updated)
    all_analyses_model.updated.connect(mr_view_model.on_all_analyses_updated)

    committed_analyses_model.updated.connect(final_plot_view_model.on_committed_analyses_updated)

    suggested_ions_model.updated.connect(working_plot_view_model.on_ions_updated)
    suggested_ions_model.updated.connect(main_window.on_ions_updated)

    analyses_view_model = viewmodels.AnalysesViewModel()
    analyses_view_model.updated.connect(main_window.on_analyses_viewmodel_updated)

    all_analyses_model.updated.connect(analyses_view_model.on_analyses_updated)

    methods_model.updated.connect(analyses_view_model.on_methods_updated)
    methods_model.updated.connect(methods_view_model.on_methods_updated)

    metadata_model.updated.connect(main_window.on_metadata_updated)
    metadata_model.updated.connect(mr_view_model.on_metadata_updated)

    loaded_m2cs_model.prime()
    bin_size_model.prime()
    suggested_ions_model.prime()
    metadata_model.prime()

    methods = load_all_methods_from_dir('methods')
    methods_model.replace(methods)

    main_window.show()
    app.exec_()
