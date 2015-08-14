from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mainwindow
import ui_posloader
import aptread.aptload
import numpy as np
from commands import *

class loadDialog(QDialog, ui_posloader.Ui_loadDialog):

    loaded=pyqtSignal()

    # METHODS = {
    #     "Manual": {},
    #     TheOnlyMethodWeSlightlyHaveAClueAboutExceptWeDoNotKnowItsName: {
    #         max_charge_state: (type=int, label="Max Charge State"),
    #         known_elements: (type=str, label="Known Elements"),
    #
    #     }
    # }
    #
    #
    # if lineedit returns Manual()
    #     method=Manual()
    #
    # method = TheOnlyMethodWeSlightlyHaveAClueAboutExceptWeDoNotKnowItsName(
    #     max_charge_state: 12,
    #     known_elements: "whateverthepersontyped",
    #
    # )
    #
    # method = Manual()


    def __init__(self, dataset, undostack, parent=None):
        super(loadDialog, self).__init__(parent)
        self.setupUi(self)
        self.posButton.setDefault(True)

        self.undoStack=undostack
        self.dataset=dataset
        self._posFilename=''
        self._rangemethod=-1

    @pyqtSignature("") # Must be included even if ""
    # as the textEdited() signal's argument is not optional
    def on_posButton_clicked(self):
        self._posFilename=QFileDialog.getOpenFileName(self,"Open .pos",'', 'POS (*.pos)')
        self.posLabel.setText(self._posFilename) #TODO Set maximum length

    @pyqtSignature("int")
    def on_rangemethodComboBox_activated(self, cb_idx):
        self._rangemethod=cb_idx
        self.loadButton.setEnabled(True) #TODO change so that enables only after all required fields are filled
        self.loadButton.setDefault(True)

    @pyqtSignature("")
    def on_removeButton_clicked(self): #TODO first, rename 'pushbutton' to removeButton in .ui
        pass #TODO Add row of Select pos + line edit

    @pyqtSlot()
    def on_loadButton_clicked(self):
        if self._posFilename is not None and self._rangemethod is not None and self._rangemethod is not 0:
            try:
                # WM=NPM(aptread.aptload.APData(self._posFilename))
                _knownelements=str(self.knownelementsLineEdit.text())
                _maxchargestate=abs(int(str(self.maxchargestateLineEdit.text())))

                posFilename=list(self._posFilename)
                knownelements=list(_knownelements)
                maxchargestate=_maxchargestate
                rangemethod=self._rangemethod

                # TODO make sure filenames is now a list or array with each file loaded
                commandLoad=CommandLoad(posFilename, rangemethod, self.dataset)
                self.undoStack.push(commandLoad) #Calls the 'redo' method
                #     #see https://forum.qt.io/topic/12330/qundocommand-calls-redo-on-initialization/6

                loaded.emit()
                loadDialog.reject(self) #USE done() and implement flag

            except aptread.aptload.APReadError:
                self.QErrorMessage.showMessage('Error reading pos file(s). Check files and file path.')

# class NPM():
#
#     def __init__(self, data, parent=None):
#         self.MC=data.pos.mc
#         self.LEN=len(data.pos)

if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)

    form=loadDialog()
    form.show()
    app.exec_()
