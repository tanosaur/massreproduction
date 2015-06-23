from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mainwindow
import sys
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 09:42:08 2015

@author: claratan
"""
import aptread.aptload
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import random

posFilename='/Users/claratan/OneDrive/Thesis/GUI/Step 3 Loadsave data/data/R04.pos'

class NPM():

    def __init__(self, data, parent=None):
        self.XYZ=data.pos.xyz
        self.MC=data.pos.mc
        self.LEN=len(data.pos)

class workingWidget(QWidget, ui_mainwindow.Ui_MainWindow):
    def __init__(self, data, parent=None):
        super(workingWidget, self).__init__(parent)
        self._data=data

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.hist(data, 3000, histtype='step')

        # refresh canvas
        self.canvas.draw()

RM=NPM(aptread.aptload.APData(posFilename))
xyz=RM.XYZ
mc=RM.MC
"""
#from num.array.convolve import boxcar
#sflux=boxcar()
n, bins, patches = plt.hist(RM.MC, 3000, normed=1, facecolor='green', histtype='step')
plt.xlabel('Mass to charge ratio')
plt.ylabel('Frequency')
plt.grid(True)
plt.axis([np.amin(np.amin(RM.MC)), np.amax(np.amax(RM.MC)), 0, 1])
plt.show()
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = workingWidget(RM.MC)
    main.show()

    sys.exit(app.exec_())
