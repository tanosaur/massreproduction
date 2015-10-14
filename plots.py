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
from matplotlib.transforms import blended_transform_factory
import itertools

import commands
from viewmodels import WorkingPlotRecord

rcParams['keymap.save'] = u'super+s'

PICKER_SENSITIVITY = 1.2

class WorkingFrame(QMainWindow):

    def __init__(self, analyses_model, methods_view_model, undo_stack, parent=None):
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
        self.ax_2 = self.ax.twinx()

        self._ions_for_lines = {}
        self._picked_ion = None

        self._analyses_model = analyses_model
        self._methods_view_model = methods_view_model
        self._undo_stack = undo_stack

        self._preserve_ax_limits = False
        self._old_m2cs = None


    @pyqtSlot(WorkingPlotRecord)
    def on_updated(self, record):
        self.ax_2.cla()
        self.lines = 0

        if record.m2cs:
            if self._preserve_ax_limits:
                def _(ax):
                    cur_xlim = ax.get_xlim()
                    cur_ylim = ax.get_ylim()
                    ax.set_xlim(cur_xlim)
                    ax.set_ylim(cur_ylim)

                _(self.ax)
                _(self.ax_2)

            if self._old_m2cs != record.m2cs:
                self._old_m2cs = record.m2cs

                self.ax.cla()
                self.ax.hist(record.m2cs, record.bin_size.value, color = 'k', histtype='step')
                self.ax.set_yscale('log')
                self.ax.set_xlabel('Da')
                self.ax.set_ylabel('Counts')
                self.canvas.draw()
                self._preserve_ax_limits = True

        if record.ions:

            trans = blended_transform_factory(self.ax.transData, self.ax.transAxes)

            colors=itertools.cycle(list('bygrcm'))

            element_keyfunc = lambda x: x.isotope.element
            sorted_ions = sorted(record.ions, key=element_keyfunc)

            for element, ions in itertools.groupby(sorted_ions, key=element_keyfunc):
                line_color=next(colors)

                for ion in ions:
                    y_height = ion.isotope.abundance/100
                    line = self.ax_2.axvline(ion.mass_to_charge, ymax=y_height, color=line_color, picker=PICKER_SENSITIVITY, label=ion.name)
                    self._ions_for_lines[line] = ion
                    self.ax_2.annotate(ion.name, xy=(ion.mass_to_charge, 0), xycoords=trans, xytext=(ion.mass_to_charge, y_height+0.04), textcoords=trans, fontsize='small', ha='center', va='center', picker=PICKER_SENSITIVITY)

        if record.analyses:

            for ion, analysis in record.analyses.items():
                start, end = analysis.range
                if start == end: #TODO make safer than this
                    line = self.ax_2.axvline(ion.mass_to_charge, color='k', picker=PICKER_SENSITIVITY, label=ion.name)
                    self._ions_for_lines[line] = ion
                else:
                    self.ax_2.axvspan(start, end, facecolor=analysis.color, alpha=0.5)

        self.canvas.draw()

    def on_key_press(self, event):
        key_press_handler(event, self.canvas, self.mpl_toolbar)

        if event.key == 'a':
            command = commands.AddIonsToTable([self._picked_ion], self._analyses_model)
            self._undo_stack.push(command)
        if event.key == 'm':
            pass
        if event.key == 's':
            command = commands.SelectMethod(self._picked_ion, 'Manual', self._analyses_model, self._methods_view_model)
            self._undo_stack.push(command)
            self._span_selector = SpanSelector(self.ax_2,self.on_span_select,'horizontal', minspan=0.0001, span_stays=True, useblit=True, rectprops=dict(alpha=0.5))
            QApplication.setOverrideCursor(QCursor(Qt.IBeamCursor))
        if event.key == 'c':
            self._update_manual_range_for_ion(self._current_span)
            self._span_selector = None
            QApplication.restoreOverrideCursor()

    def on_pick(self, event):
        if isinstance(event.artist, Line2D):
            line=event.artist
            ion = self._ions_for_lines[line]
            self.ax_2.axvline(line.get_xdata()[0], color=line.get_color(), linewidth=line.get_lw()*3)
            self._picked_ion = ion
            line.remove()
            self.canvas.draw()

    def on_span_select(self,x0,x1):
        self._current_span = (x0, x1)

    def _update_manual_range_for_ion(self, current_span):
        start, end = current_span
        _picked_ion = self._picked_ion
        command = commands.UpdateManualRange(_picked_ion, start, end, self._analyses_model)
        self._undo_stack.push(command)
