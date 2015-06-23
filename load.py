from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mainwindow
import ui_posloader
import aptread.aptload
import numpy as np

class loadDialog(QDialog, ui_posloader.Ui_loadDialog): # Multiple inheritance
    # Rarely need in Python, but useful in this case

    loaded=pyqtSignal(np.ndarray, int) #passing array of MC and LEN

    def __init__(self, parent=None):
        super(loadDialog, self).__init__(parent)
        self.setupUi(self)
        self._posFilename=''

    @pyqtSignature("") # Must be included even if ""
    # as the textEdited() signal's argument is not optional
    def on_posButton_clicked(self):
        self._posFilename=QFileDialog.getOpenFileName(self,"Open .pos",'', 'POS (*.pos)')
        self.posLabel.setText(self._posFilename) #TODO Set maximum length
        self.loadButton.setEnabled(True)

    @pyqtSignature("")
    def on_addButton_clicked(self):
        PASS #TODO Add row of Select pos + line edit

    @pyqtSignature("")
    def on_loadButton_clicked(self):
        if self._posFilename is not None:
            try:
                WM=NPM(aptread.aptload.APData(self._posFilename))
                self.loaded.emit(WM.MC, WM.LEN)
                loadDialog.reject(self) #USE done() and implement flag
            except aptread.aptload.APReadError:
                self.QErrorMessage.showMessage('Error reading pos file(s). Check files and file path.')


class NPM():

    def __init__(self, data, parent=None):
        self.XYZ=data.pos.xyz
        self.MC=data.pos.mc
        self.LEN=len(data.pos)

        #print(type(self.XYZ), type(self.MC), type(self.LEN))
        #np.ndarray, np.ndarray, int


if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)

    form=loadDialog()
    form.show()
    app.exec_()
