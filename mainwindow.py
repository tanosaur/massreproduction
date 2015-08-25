from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow, QUndoStack, QUndoView, QApplication, QFileDialog
import sys
import ui_mainwindow
from plots import WorkingFrame, RangedFrame
import commands
import models

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):

    def __init__(self, loaded_m2c_model, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._loaded_m2c_model = loaded_m2c_model

        self.undoStack = QUndoStack(self)
        history_view = QUndoView(self.undoStack, parent=self.stackView)
        history_view.setEmptyLabel('New program')

    @pyqtSlot(models.BinSizeRecord)
    def on_bin_size_updated(self, bin_size):
        self.binsizeSpinBox.setMaximum(bin_size.maximum)
        self.binsizeSpinBox.setMinimum(bin_size.minimum)
        self.binsizeSpinBox.setValue(bin_size.value)

    @pyqtSlot()
    def on_actionLoad_triggered(self):
        pos_filename=QFileDialog.getOpenFileName(self,"Open .pos file",'', 'POS (*.pos)')
        if pos_filename:
            command = commands.LoadM2C(pos_filename, self._loaded_m2c_model)
            self.undoStack.push(command)

    @pyqtSlot(int)
    def on_binsizeSpinBox_valueChanged(self, bin_size_value):
        command = command.BinSizeValueChange(bin_size_value, self.bin_size_model)
        self.undoStack.push(command)

    @pyqtSlot()
    def on_suggestButton_clicked(self):
        commandSuggest=CommandSuggest(
            str(self.knownelementsLineEdit.text()),
            abs(int(str(self.maxchargestateLineEdit.text()))),
            self.suggest_model
        )
        self.undoStack.push(commandSuggest)

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

    main_window = MainWindow(loaded_m2c_model)
    working_frame = WorkingFrame(parent=main_window.workingFrame)
    ranged_frame = RangedFrame(parent=main_window.rangedFrame)

    working_plot_view_model = models.WorkingPlotViewModel()

    working_plot_view_model.updated.connect(working_frame.on_updated)
    loaded_m2c_model.updated.connect(working_plot_view_model.on_m2c_updated)
    # LoadedM2CModel -> FinalPlotViewModel.m2c
    bin_size_model.updated.connect(working_plot_view_model.on_bin_size_updated)
    # BinSizeModel -> FinalPlotViewModel.bin_size
    # AllRangesModel -> WorkingPlotViewModel.ranges
    # AllRangesModel -> CommittedRangesModel
    # CommittedRangesModel -> FinalPlotViewModel.ranges
    # SuggestedIonsModel -> WorkingPlotViewModel.ions
    # SuggestedIonsModel -> SuggestedIonsViewModel
    # AllRangesModel -> AnalysesModel
    # AnalysesModel -> AnalysesTableViewModel

    loaded_m2c_model.prime()
    bin_size_model.prime()

    main_window.show()
    app.exec_()
