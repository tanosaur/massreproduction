from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow, QUndoStack, QUndoView, QApplication, QFileDialog
import sys
import ui_mainwindow
from plots import WorkingFrame, RangedFrame
import commands
import models

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):

    def __init__(self, loaded_m2c_model, bin_size_model, suggested_ions_model, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._loaded_m2c_model = loaded_m2c_model
        self._bin_size_model = bin_size_model
        self._suggested_ions_model = suggested_ions_model

        self.undoStack = QUndoStack(self)
        history_view = QUndoView(self.undoStack, parent=self.stackView)
        history_view.setEmptyLabel('New program')

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
        command=SuggestChange(
            str(self.knownelementsLineEdit.text()),
            abs(int(str(self.maxchargestateLineEdit.text()))),
            self._suggested_ions_model
        )
        self.undoStack.push(command)

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self.undoStack.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self.undoStack.redo()

    @pyqtSlot(str)
    def on_maxchargestateLineEdit_textEdited(self):
        enable=not self.maxchargestateLineEdit.text().isEmpty()
        self.suggestButton.setEnabled(enable) #TODO initially disable this
        self.suggestButton.setFocus()

if __name__ == '__main__':
    app=QApplication(sys.argv)

    loaded_m2c_model = models.LoadedM2CModel()
    bin_size_model = models.BinSizeModel()
    suggested_ions_model = models.SuggestedIonsModel()

    main_window = MainWindow(loaded_m2c_model, bin_size_model, suggested_ions_model)
    working_frame = WorkingFrame(parent=main_window.workingFrame)
    ranged_frame = RangedFrame(parent=main_window.rangedFrame)

    working_plot_view_model = models.WorkingPlotViewModel()
    final_plot_view_model = models.FinalPlotViewModel()

    working_plot_view_model.updated.connect(working_frame.on_updated)
    loaded_m2c_model.updated.connect(working_plot_view_model.on_m2c_updated)

    final_plot_view_model.updated.connect(ranged_frame.on_updated)
    loaded_m2c_model.updated.connect(final_plot_view_model.on_m2c_updated)

    bin_size_model.updated.connect(main_window.on_bin_size_updated)
    bin_size_model.updated.connect(working_plot_view_model.on_bin_size_updated)
    bin_size_model.updated.connect(final_plot_view_model.on_bin_size_updated)

    all_ranges_model = models.AllRangesModel()
    committed_ranges_model = models.CommittedRangesModel()

    all_ranges_model.updated.connect(working_plot_view_model.on_ranges_updated)
    all_ranges_model.updated.connect(committed_ranges_model.on_ranges_updated)

    committed_ranges_model.updated.connect(final_plot_view_model.on_ranges_updated)

    suggested_ions_view_model = SuggestedIonsViewModel()

    suggested_ions_model.updated.connect(working_plot_view_model.on_ions_updated)
    suggested_ions_model.updated.connect(suggested_ions_view_model.on_ions_updated)

    analyses_model = AnalysesModel()
    analyses_table_view_model = AnalysesTableViewModel()

    all_ranges_model.updated.connect(analyses_model.on_ranges_updated)
    analyses_model.updated.connect(analyses_table_view_model.on_analyses_updated)

    loaded_m2c_model.prime()
    bin_size_model.prime()

    main_window.show()
    app.exec_()
