from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MyForm(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(100, 150, 300, 120)
        self.setWindowTitle("start typing")
        line_edit = QLineEdit(self)
        label = QLabel(self)
        # connect line_edit to label
        # update label each time the text has been edited
        line_edit.connect(line_edit, SIGNAL("textEdited(QString)"), label.setText)
        # use a grid layout for the widgets
        grid = QGridLayout()
        # addWidget(widget, row, column, rowSpan, columnSpan)
        grid.addWidget(line_edit, 0, 0, 1, 1)
        grid.addWidget(label, 1, 0, 1, 1)
        self.setLayout(grid)
app =  QApplication([])
form = MyForm()
form.show()
app.exec_()
