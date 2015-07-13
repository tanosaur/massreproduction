from __future__ import print_function
from PyQt4 import QtCore, QtGui

import ui_untitled

import numpy as np
import random

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import key_press_handler

from matplotlib.widgets import SpanSelector
from itertools import cycle

import sys
import matplotlib
matplotlib.rcParams['keymap.pan'] = u'ctrl+p'

"""
          u'keymap.all_axes': [u'a'],
          u'keymap.back': [u'left', u'c', u'backspace'],
          u'keymap.forward': [u'right', u'v'],
          u'keymap.fullscreen': [u'f', u'ctrl+f'],
          u'keymap.grid': [u'g'],
          u'keymap.home': [u'h', u'r', u'home'],
          u'keymap.pan': [u'p'],
          u'keymap.quit': [u'ctrl+w', u'cmd+w'],
          u'keymap.save': [u's', u'ctrl+s'],
          u'keymap.xscale': [u'k', u'L'],
          u'keymap.yscale': [u'l'],
          u'keymap.zoom': [u'o'],
"""

class MainWindow(QtGui.QMainWindow, ui_untitled.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # intialize the window
        self.setupUi(self)
        self.plotWidget = widget(parent=self.frame)


class widget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(widget, self).__init__(parent)
        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(parent)
        self.canvas.setFocus()
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, parent)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        # random data
        data = [random.random() for i in range(10)]
        t=np.arange(180)
        value=(20*np.sin((np.pi/2)*(t/22.0)) + 25 * np.random.random((len(t),))+50)
        # create an axis
        self.ax = self.figure.add_subplot(111)

        # # discards the old graph
        # ax.hold(False)
        #
        # # plot data
        self.ax.step(t,value)
        self.colors=cycle(list('rybmc'))

        self.ss=SpanSelector(self.ax,self.onselect,'horizontal')
        # self.canvas.draw()

    def onselect(self,x0,x1):
        self.ax.axvspan(x0,x1, facecolor=next(self.colors), alpha=0.5)
        print(x0,x1)
        self.figure.canvas.draw_idle() #keeps the selection drawn on

    def on_key_press(self, event):
        print('you pressed', event.key)
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.canvas, self.toolbar)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    main = MainWindow()
    main.show()

    s = main.frame.size()
    main.plotWidget.setGeometry(1, 1, s.width() - 2, s.height() - 2)

    sys.exit(app.exec_())
