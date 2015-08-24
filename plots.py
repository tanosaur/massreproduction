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
from collections import namedtuple

rcParams['keymap.save'] = u'super+s'

PlotParameters = namedtuple('PlotParameters', 'm2c bin_size suggested_ions')

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
        # self.canvas.mpl_connect('pick_event', self.onpick)
        # self.canvas.mpl_connect('button_press_event', self.onclick)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        vbox.addWidget(self.mpl_toolbar)
        parent.setLayout(vbox)

        self._plot_parameters = PlotParameters([], 1, [])
        self.ax = self.fig.add_subplot(111)
        self._make_plot(self._plot_parameters)

        self._picked_object = None

    # def onpick(event):
    #     if isinstance(event.artist, SpanSelector):
    #         thisline = event.artist
    #         xdata = thisline.get_xdata()
    #         ydata = thisline.get_ydata()
    #         ind = event.ind
    #         print('onpick:', zip(np.take(xdata, ind), np.take(ydata, ind)))
    #         #this doesn't work
    #     elif isinstance(event.artist, Text):
    #         text = event.artist
    #         print('onpick text:', text.get_text())

    # def onclick(event):
    #     print ('button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata))

    def _cache_plot_parameters(self, **kwargs):
        # Store most recently passed values
        self._plot_parameters = self._plot_parameters._replace(**kwargs)
        return self._plot_parameters

    def _make_plot(self, plot_parameters):
        self.ax.cla()

        self.lines = 0

        if plot_parameters.m2c:
            self.ax.hist(plot_parameters.m2c, plot_parameters.bin_size, histtype='step')

        self.ax.set_yscale('log')

        if plot_parameters.suggested_ions:
            # self.ax.lines=[] # Necessary to clear the lines and labels for every undo/redo.
            # self.ax.texts=[]
            colors=cycle(list('rybmc'))

            for element in plot_parameters.suggested_ions.keys():
                line_color=next(colors)
                ions=plot_parameters.suggested_ions[element]
                for ion in range(len(ions)):
                    label, m2c, abundance = ions[ion]
                    self.ax.axvline(m2c, color=line_color, picker=0.5)
                    self.ax.text(m2c, 100, label, fontsize=10, picker=0.3)

        self.canvas.draw()

    @pyqtSlot(list)
    def on_m2c_updated(self, m2c):
        plot_parameters = self._cache_plot_parameters(m2c=m2c)
        self._make_plot(plot_parameters)

    @pyqtSlot(int)
    def on_bin_size_updated(self,bin_size):
        # save frame zoom
        # save any lines on suggest
        plot_parameters = self._cache_plot_parameters(bin_size=bin_size)
        self._make_plot(plot_parameters)

    @pyqtSlot(dict)
    def on_suggest_updated(self,suggested_ions):
        plot_parameters = self._cache_plot_parameters(suggested_ions=suggested_ions)
        self._make_plot(plot_parameters)

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
        self.ax.hold(False)
        self.make_plot()

    def make_plot(self,m2cs=[], bins=1000):
        if not any(m2cs):
            self.ax.hist(np.arange(1,3), bins, histtype='step')
            self.ax.cla()
        else:
            self.colors=cycle(list('rybmc'))
            self.ax.hist(m2cs, bins, histtype='step')
            self.ax.set_yscale('log')
        self.canvas.draw()
