from PyQt4.QtCore import pyqtSlot, Qt, pyqtProperty, QModelIndex, QEvent, QObject, QPoint
from PyQt4.QtGui import QMainWindow, QDialog, QUndoStack, QUndoView, QApplication, QFileDialog, QStandardItemModel, QItemSelection, QStandardItem, QComboBox, QStyledItemDelegate, QLabel, QItemSelectionModel, QFocusEvent, QMenu, QKeySequence, QShortcut

import sys
import ui_mainwindow
import ui_toolsdialog
import ui_exporterrordialog
from plots import WorkingFrame
import viewmodels
import commands
import models
import itertools
from methods import load_all_methods_from_dir

class ExportErrorDialog(QDialog, ui_exporterrordialog.Ui_ExportErrorDialog):
    def __init__(self, parent=None):
        super(ExportErrorDialog, self).__init__(parent)
        self.setupUi(self)

class ToolsDialog(QDialog, ui_toolsdialog.Ui_ToolsDialog):
    def __init__(self, undo_stack, suggested_ions_model, analyses_model, parent=None):
        super(ToolsDialog, self).__init__(parent)
        self.setupUi(self)

        self._undo_stack = undo_stack

        self._suggested_ions_model = suggested_ions_model
        self._analyses_model = analyses_model

        self._qmodel=None

        history_view = QUndoView(self._undo_stack, parent=self.stackView)
        history_view.setEmptyLabel('New program')

    @pyqtSlot()
    def on_suggestButton_clicked(self):
        command = commands.SuggestIons(
            self.knownelementsLineEdit.text(),
            abs(int(self.maxchargestateLineEdit.text())),
            self._suggested_ions_model
        )
        self._undo_stack.push(command)
        self.addionsButton.setFocus()
        self.clearionsButton.setEnabled(True)

    @pyqtSlot()
    def on_addionsButton_clicked(self):
        qmodel_indices=self.ionlistTree.selectedIndexes()
        # TODO fix so filter not needed, otherwise, leave comment explanation
        ions=list(filter(None,[self._qmodel.data(index,32) for index in qmodel_indices]))
        command = commands.AddIonsToTable(ions, self._analyses_model)
        self._undo_stack.push(command)

    @pyqtSlot()
    def on_clearionsButton_clicked(self):
        self._suggested_ions_model.clear()

    @pyqtSlot(str)
    def on_maxchargestateLineEdit_textEdited(self):
        self.suggestButton.setEnabled(True)
        self.suggestButton.setFocus()

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
        self._qmodel=qmodel


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


class MainWindow(QMainWindow, ui_mainwindow.Ui_MassRep):

    def __init__(self, tools_dialog, export_error_dialog, undo_stack, loaded_m2cs_model, bin_size_model, analyses_model, methods_view_model, metadata_model, export_view_model, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._tools_dialog = tools_dialog
        self._export_error_dialog = export_error_dialog

        self._undo_stack = undo_stack
        self._loaded_m2cs_model = loaded_m2cs_model
        self._bin_size_model = bin_size_model
        self._analyses_model = analyses_model
        self._methods_model = methods_model
        self._metadata_model = metadata_model

        self._methods_view_model = methods_view_model
        self._export_view_model = export_view_model

    @pyqtSlot(models.BinSizeRecord)
    def on_bin_size_updated(self, bin_size):
        self.binsizeSlider.setMaximum(bin_size.maximum)
        self.binsizeSlider.setMinimum(bin_size.minimum)
        self.binsizeSlider.setValue(bin_size.value)

    @pyqtSlot()
    def on_actionLoad_triggered(self):
        pos_filename=QFileDialog.getOpenFileName(self,"Open .pos file",'', 'POS (*.pos)')
        if pos_filename:
            command = commands.LoadPOS(pos_filename, self._loaded_m2cs_model, self._metadata_model)
            self._undo_stack.push(command)

    @pyqtSlot(int)
    def on_binsizeSlider_sliderMoved(self, bin_size_value):
        command = commands.BinSizeValueChange(bin_size_value, self._bin_size_model)
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
        self.rangedTable.setContextMenuPolicy(3)
        self.rangedTable.customContextMenuRequested.connect(self.context_menu_requested)
        shortcut = QShortcut(QKeySequence('Del'), self.rangedTable, self.delete_ion,self.delete_ion, context=0)

    @pyqtSlot(QPoint)
    def context_menu_requested(self, point):
        if self.rangedTable.selectedIndexes():
            menu = QMenu(self)
            delete_analysis = menu.addAction('Delete')
            delete_analysis.triggered.connect(self.delete_ion)
            menu.exec_(self.mapToGlobal(point))

    @pyqtSlot()
    def delete_ion(self):
        selected_indexes = self.rangedTable.selectedIndexes()
        selected_ions = []
        for index in selected_indexes:
            if index.column() == 0:
                selected_ions.append(index.data(Qt.UserRole))

        command = commands.DeleteIon(selected_ions, self._analyses_model)
        self._undo_stack.push(command)

    @pyqtSlot(QStandardItem)
    def on_qmodel_itemChanged(self, item):
        index = item.index()
        ion_index = index.sibling(index.row(), 0)
        ion = ion_index.data(Qt.UserRole)

        if item.column() == 1:
            method_index = index.sibling(index.row(), 1)
            method_name = method_index.data(Qt.DisplayRole)

            command = commands.SelectMethod(ion, method_name, self._analyses_model, self._methods_view_model)
            self._undo_stack.push(command)

            print("Change: %s: %s" % (ion.name, method_name))

        elif item.column() == 2 or item.column() == 3:
            start_index = index.sibling(index.row(), 2)
            end_index = index.sibling(index.row(), 3)

            start = start_index.data(Qt.DisplayRole)
            end = end_index.data(Qt.DisplayRole)

            command = commands.SelectMethod(ion, 'Manual', self._analyses_model, self._methods_view_model)
            self._undo_stack.push(command)

            command = commands.UpdateManualRange(ion, start, end, self._analyses_model)
            self._undo_stack.push(command)

            print("Change: %s: %s" % (ion.name, 'Manual'))
            print("Change: %s: %s - %s" % (ion.name, start, end))

        elif item.column() == 4:
            reason_index = index.sibling(index.row(), 4)
            reason = reason_index.data(Qt.DisplayRole)

            command = commands.UpdateReason(ion, reason, self._analyses_model)
            self._undo_stack.push(command)

            print("Change: %s: %s" % (ion.name, reason))

    @pyqtSlot()
    def on_action_ExportAsJSON_triggered(self):
        json_filename=QFileDialog.getSaveFileName(self, 'Export file as .json','','JSON (*.json)')
        command = commands.ExportAsJSON(json_filename, self._export_view_model)
        self._undo_stack.push(command)

    @pyqtSlot()
    def on_action_ExportAsRNG_triggered(self):
        rng_filename=QFileDialog.getSaveFileName(self, 'Export file as .rng','','RNG (*.rng)')
        command = commands.ExportAsRNG(rng_filename, self._export_view_model)
        self._undo_stack.push(command)

    @pyqtSlot()
    def on_export_error(self):
        error_dialog = self._export_error_dialog.exec_()
        QApplication.beep()

    @pyqtSlot()
    def on_action_LoadJSON_triggered(self):
        mr_filename=QFileDialog.getOpenFileName(self,"Open .json file",'', 'JSON (*.json)')
        if mr_filename:
            command = commands.ImportJSON(mr_filename, self._export_view_model, self._analyses_model, self._metadata_model)
            self._undo_stack.push(command)

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self._undo_stack.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self._undo_stack.redo()

    @pyqtSlot()
    def on_actionTools_triggered(self):
        self._tools_dialog.show()

    @pyqtSlot()
    def on_experimentIDLineEdit_editingFinished(self):
        experiment_ID = self.experimentIDLineEdit.text()
        command = commands.UpdateExperimentID(experiment_ID, self._metadata_model)
        self._undo_stack.push(command)

    @pyqtSlot()
    def on_experimentdescriptionLineEdit_editingFinished(self):
        experiment_description = self.experimentdescriptionLineEdit.text()
        command = commands.UpdateExperimentDescription(experiment_description, self._metadata_model)
        self._undo_stack.push(command)

    @pyqtSlot(tuple)
    def on_metadata_updated(self, metadata):
        self.experimentIDLineEdit.setText(metadata.ID)
        self.experimentdescriptionLineEdit.setText(metadata.description)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    print('Loading MassRep...')

    undo_stack = QUndoStack()

    loaded_m2cs_model = models.M2CModel()
    bin_size_model = models.BinSizeModel()
    suggested_ions_model = models.SuggestedIonsModel()
    methods_model = models.MethodsModel()
    analyses_model = models.AnalysesModel()
    metadata_model = models.MetadataModel()

    working_plot_view_model = viewmodels.WorkingPlotViewModel()
    methods_view_model = viewmodels.MethodsViewModel()
    export_view_model = viewmodels.ExportViewModel()

    tools_dialog = ToolsDialog(undo_stack, suggested_ions_model, analyses_model)
    export_error_dialog = ExportErrorDialog()
    main_window = MainWindow(tools_dialog, export_error_dialog, undo_stack, loaded_m2cs_model, bin_size_model, analyses_model, methods_view_model, metadata_model, export_view_model)
    working_frame = WorkingFrame(analyses_model, methods_view_model, undo_stack, parent=main_window.workingFrame)

    working_plot_view_model.updated.connect(working_frame.on_updated)
    working_plot_view_model.loaded.connect(working_frame.on_loaded)
    loaded_m2cs_model.updated.connect(working_plot_view_model.on_m2cs_updated)
    loaded_m2cs_model.updated.connect(methods_view_model.on_m2cs_updated)

    bin_size_model.updated.connect(main_window.on_bin_size_updated)
    bin_size_model.updated.connect(working_plot_view_model.on_bin_size_updated)
    bin_size_model.updated.connect(methods_view_model.on_bin_size_updated)

    analyses_model.updated.connect(working_plot_view_model.on_analyses_updated)
    analyses_model.updated.connect(export_view_model.on_analyses_updated)

    suggested_ions_model.updated.connect(working_plot_view_model.on_ions_updated)
    suggested_ions_model.updated.connect(tools_dialog.on_ions_updated)

    analyses_view_model = viewmodels.AnalysesViewModel()
    analyses_view_model.updated.connect(main_window.on_analyses_viewmodel_updated)

    analyses_model.updated.connect(analyses_view_model.on_analyses_updated)

    methods_model.updated.connect(analyses_view_model.on_methods_updated)
    methods_model.updated.connect(methods_view_model.on_methods_updated)

    metadata_model.updated.connect(main_window.on_metadata_updated)
    metadata_model.updated.connect(export_view_model.on_metadata_updated)

    export_view_model.export_error.connect(main_window.on_export_error)

    loaded_m2cs_model.prime()
    bin_size_model.prime()
    suggested_ions_model.prime()
    metadata_model.prime()

    methods = load_all_methods_from_dir('methods')
    methods_model.replace(methods)

    main_window.show()
    print('Let us begin.')
    app.exec_()
