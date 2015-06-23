# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import numpy as np

import matplotlib
import sys
# specify the use of PySide
matplotlib.rcParams['backend.qt4'] = "PyQt4"

# import the figure canvas for interfacing with the backend
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg \
                                                                as FigureCanvas

# import 3D plotting
from mpl_toolkits.mplot3d import Axes3D    # @UnusedImport
from matplotlib.figure import Figure


# Auto-generated code from QT Designer ----------------------------------------

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 497)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit = QtGui.QLineEdit(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(
                            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
                                self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        spacerItem = QtGui.QSpacerItem(
                20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.frame_plot = QtGui.QFrame(self.centralwidget)
        self.frame_plot.setMinimumSize(QtCore.QSize(500, 0))
        self.frame_plot.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_plot.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_plot.setObjectName("frame_plot")
        self.horizontalLayout_2.addWidget(self.frame_plot)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate(
            "MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow",
                    "This is a qlabel.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow",
            "And this is another one.", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("MainWindow",
                    "Text goes here.", None, QtGui.QApplication.UnicodeUTF8))

# Auto-generated code from QT Designer ----------------------------------------

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # intialize the window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # create the matplotlib widget and put it in the frame on the right
        self.ui.plotWidget = Mpwidget(parent=self.ui.frame_plot)

class Mpwidget(FigureCanvas):
    def __init__(self, parent=None):

        self.figure = Figure(facecolor=(0, 0, 0))
        super(Mpwidget, self).__init__(self.figure)
        self.setParent(parent)

        # plot random 3D data
        self.axes = self.figure.add_subplot(111, projection='3d')
        self.data = np.random.random((3, 100))
        self.axes.plot(self.data[0, :], self.data[1, :], self.data[2, :])

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()

    # adjust the frame size so that it fits right after the window is shown
    s = mw.ui.frame_plot.size()
    mw.ui.plotWidget.setGeometry(1, 1, s.width() - 2, s.height() - 2)

    sys.exit(app.exec_())
