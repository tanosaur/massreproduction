import ui_dialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Dialog(QDialog, ui_dialog.Ui_Dialog):

    origAS=self.lineEdit.text()
    currentAS=origAS

    def __init__(self,parent=None):
        super(Dialog,self).__init__(parent)

        # From ui_dialog.py - creates the form in .ui file and
        # calls QtCore.QMetaObject.connectSlotsByName()
        # to set up signal-slot connections by naming convention
        self.setupUi(self)

        # All buttons initially disabled until enabled
        self.updateUi()

    #LOAD AND ENABLE

    def updateUi(self):
        enable=not self.lineEdit.text() # In Python, empty strings
        # are 'falsy' https://docs.python.org/2/library/stdtypes.html
        # Enables the Find, Replace, and Replace All buttons
        self.D000aButton.setEnabled(enable)
        self.D000bButton.setEnabled(enable)
        self.D000cButton.setEnabled(enable)

    @pyqtSignature("QString") # Decorator to specify naming convention
    def on_LineEdit_textEdited(self,text):
        self.updateUi()

    # 000 Program Run

    # @pyqtSignature("") # Must be included even if ""
    # # as the clicked() signal's argument is not optional
    # def on_D000aButton_clicked(self):
    #     #RUN 000a
    #

    def read(self):
        return self.lineEdit.text()

    @pyqtSignature("")
    def on_D000bButton_clicked(self):
        # RUN 000b
        text_send=self.lineEdit.text()# Read analysis state
        self.outputLabel.clear() # Update available plots/tables
        self.outputLabel.setText(text_send)

    @pyqtSignature("")
    def on_D000cButton_clicked(self):
        #RUN 000c
        # Update analysis state
        change_AS=current_AS[-1]
        current_AS=current_AS[:-1] # New analysis state
        self.outputLabel.clear()
        self.outputLabel.setText(current_AS)



# TESTING
if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)
    form=Dialog()
    form.show()
    app.exec_()
