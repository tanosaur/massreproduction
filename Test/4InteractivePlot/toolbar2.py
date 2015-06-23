from __future__ import print_function
import ui_untitled
import sys
import aptread.aptload
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class NPM():

    def __init__(self, data, parent=None):
        self.XYZ=data.pos.xyz
        self.MC=data.pos.mc
        self.LEN=len(data.pos)


class MainWindow(QMainWindow,ui_untitled.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #self.x, self.y = self.get_data()

        self.setupUi(self)
        self.plotWidget = widget(parent=self.frame)
        self.plotWidget=widget(parent=self.widget)

class widget(QMainWindow, NPM):
    def __init__(self, parent=None):
        super(widget, self).__init__(parent)

        posFilename='/Users/sojung/OneDrive/Thesis/GUI/Step 3 Loadsave data/data/R04.pos'

        self.WM=NPM(aptread.aptload.APData(posFilename))

        self.data=self.WM.MC
        self.bins=3000

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()

        self.mpl_toolbar = NavigationToolbar(self.canvas, parent)

        self.canvas.mpl_connect('key_press_event', self.on_key_press)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        vbox.addWidget(self.mpl_toolbar)
        self.setLayout(vbox)

        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.hist(self.data,self.bins,histtype='step')
        self.canvas.draw()


    def on_key_press(self, event):
        print('you pressed', event.key)
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.canvas, self.mpl_toolbar)


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    s=form.frame.size()
    form.plotWidget.setGeometry(1, 1, s.width() - 2, s.height() - 2)
    app.exec_()


if __name__ == "__main__":
    main()
