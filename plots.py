from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
from matplotlib.backends import qt_compat
from matplotlib.backend_bases import key_press_handler
from matplotlib.widgets import SpanSelector
from matplotlib.lines import Line2D
from matplotlib import rcParams, patheffects
import itertools
from viewmodels import WorkingPlotRecord, FinalPlotRecord

rcParams['keymap.save'] = u'super+s'

PICKER_SENSITIVITY = 1.2

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

    @pyqtSlot(WorkingPlotRecord)
    def on_updated(self, record):

        self.ax.cla()

        self.lines = 0

        if record.m2cs:
            self.ax.hist(record.m2cs, record.bin_size.value, histtype='step')

        self.ax.set_yscale('log')

        if record.ions:
            colors=itertools.cycle(list('rybmc'))

            element_keyfunc = lambda x: x.isotope.element
            sorted_ions = sorted(record.ions, key=element_keyfunc)

            for element, ions in itertools.groupby(sorted_ions, key=element_keyfunc):
                line_color=next(colors)

                for ion in ions:
                    self.ax.axvline(ion.mass_to_charge, color=line_color, picker=PICKER_SENSITIVITY)
                    self.ax.text(ion.mass_to_charge, 100, ion.name, fontsize=10, picker=PICKER_SENSITIVITY)

        if record.all_analyses:

            for ion, analysis in record.all_analyses.items():
                start, end = analysis.range
                if analysis.method == 'Manual':
                    self.ax.axvline(ion.mass_to_charge, color='k', picker=PICKER_SENSITIVITY)
                else:
                    self.ax.axvspan(start, end, facecolor=analysis.color, alpha=0.5)

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
        if isinstance(event.artist, Line2D):
            line=event.artist
            self.ax.axvline(line.get_xdata()[0], color=line.get_color(), linewidth=line.get_lw()*3)
            line.remove()
            self.canvas.draw()


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

        self.ax.cla()

        self.lines = 0

        if record.m2cs:
            self.ax.hist(record.m2cs, record.bin_size.value, histtype='step')

        if record.committed_analyses:
            #TODO adjust colors so colors are per element (sort by element..?)
            for ion, analysis in record.committed_analyses.items():
                start, end = analysis.range
                self.ax.axvspan(start, end, ymin=0, facecolor='g', alpha=0.5)


        self.ax.set_yscale('log')
        self.canvas.draw()
