import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.buttonA = QPushButton("Button &A")
        self.buttonB = QPushButton("Button &B")
        self.label = QLabel("No button has been clicked")
        layout = QVBoxLayout()
        layout.addWidget(self.buttonA)
        layout.addWidget(self.buttonB)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.connect(self.buttonA, SIGNAL("clicked()"), self.pressedA)
        self.connect(self.buttonB, SIGNAL("clicked()"), self.pressedB)
        self.setWindowTitle("Simple")

        self.undoStack = QUndoStack(self) #Although an instance variable,
            #must still give it a parent (the dialog box) s.t. PyQt4 can clean it
            #up at the right time when the dialog box is destroyed.

        self.undoStack.undo()
        self.undoStack.redo()

    def pressedA(self):
        self.label.setText("Button A clicked")

    def pressedB(self):
        self.label.setText("Button B clicked")

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
