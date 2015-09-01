import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
from matplotlib.backends import qt_compat
from matplotlib.backend_bases import key_press_handler
from matplotlib.widgets import SpanSelector
from matplotlib import rcParams

from itertools import cycle

from viewmodels import WorkingPlotRecord, FinalPlotRecord

rcParams['keymap.save'] = u'super+s'

class WorkingFrame(QMainWindow):

    def __init__(self, parent=None):
        super(WorkingFrame, self).__init__(parent)

        self.fig=Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()

        self.mpl_toolbar = NavigationToolbar(self.canvas, parent)

        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.canvas.mpl_connect('pick_event', self.on_pick)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        vbox.addWidget(self.mpl_toolbar)
        parent.setLayout(vbox)

        self.ax = self.fig.add_subplot(111)

        self._picked_object = None

    @pyqtSlot(WorkingPlotRecord)
    def on_updated(self, record):
        print('working plot updated')

        self.ax.cla()

        self.lines = 0

        if record.m2c:
            self.ax.hist(record.m2c, record.bin_size.value, histtype='step')

        self.ax.set_yscale('log')

        if record.ions:
            colors=cycle(list('rybmc'))

            for ion in record.ions:
                line_color=next(colors)
                self.ax.axvline(ion.mass_to_charge, color=line_color, picker=0.5)
                self.ax.text(ion.mass_to_charge, 100, ion.name, fontsize=10, picker=0.3)

        if record.ranges:
            pass

        self.canvas.draw()


    def on_span_select(self,x0,x1):
        self.ax.axvspan(x0,x1, facecolor='c', alpha=0.5)
        print(x0,x1)

    def on_key_press(self, event):
        print('You pressed %s' % (event.key))
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.canvas, self.mpl_toolbar)

        if event.key == 's':
            self.ss=SpanSelector(self.ax,self.on_span_select,'horizontal', minspan=0.0001, span_stays=True)

    def on_pick(self, event):
        self._picked_object=event.artist


class RangedFrame(QMainWindow):

    def __init__(self, parent=None):

        super(RangedFrame, self).__init__(parent)

        self.fig=Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        parent.setLayout(vbox)

        self.ax=self.fig.add_subplot(111)

    @pyqtSlot(FinalPlotRecord)
    def on_updated(self, record):
        print('final plot updated')

        self.ax.cla()

        self.lines = 0

        if record.m2c:
            self.ax.hist(record.m2c, record.bin_size.value, histtype='step')

        if record.ranges:
            pass

        self.ax.set_yscale('log')
        self.canvas.draw()
