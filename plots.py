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

        self._analyses_model = analyses_model
        self._methods_view_model = methods_view_model
        self._undo_stack = undo_stack

        self.fig=Figure()
        self.canvas = FigureCanvas(self.fig)
        self.mpl_toolbar = NavigationToolbar(self.canvas, parent)

        def _set_up_canvas(canvas):
            canvas.setParent(parent)
            canvas.setFocusPolicy(Qt.StrongFocus)
            canvas.setFocus()

        def _connect_canvas_with_events(canvas):
            canvas.mpl_connect('key_press_event', self.on_key_press)
            canvas.mpl_connect('pick_event', self.on_pick)

        def _set_up_Qt_layout():
            vbox = QVBoxLayout()
            vbox.addWidget(self.canvas)
            vbox.addWidget(self.mpl_toolbar)
            parent.setLayout(vbox)

        _set_up_canvas(self.canvas)
        _connect_canvas_with_events(self.canvas)
        _set_up_Qt_layout()

        self.ax = self.fig.add_subplot(111)

        self._ions_for_lines = {}
        self._picked_ion = None

        self._old_m2cs = None
        self._old_bin_size = None

        self._current_lines = []
        self._current_line_labels = []
        self._current_spans = []

        self._preserve_ax_limits = False

    @pyqtSlot(WorkingPlotRecord)
    def on_updated(self, record):

        def _clear(plot_object):
            plot_object = list(filter(None, plot_object))
            emptied_plot_object = [_object.remove() for _object in plot_object]
            return emptied_plot_object

        def _clear_lines_and_spans():
            if self._current_spans:
                self._current_spans = _clear(self._current_spans)
            if self._current_lines:
                self._current_lines = _clear(self._current_lines)
                self._current_line_labels = _clear(self._current_line_labels)

        _clear_lines_and_spans()

        if record.m2cs:

            if self._preserve_ax_limits:

                def _set_same_ax_limits():
                    current_xlim = self.ax.get_xlim()
                    current_ylim = self.ax.get_ylim()
                    self.ax.set_xlim(current_xlim)
                    self.ax.set_ylim(current_ylim)

                _set_same_ax_limits()

            if self._old_m2cs != record.m2cs or self._old_bin_size != record.bin_size.value:

                self._old_m2cs = record.m2cs
                self._old_bin_size = record.bin_size.value

                def _plot_histogram(ax):
                    ax.hist(record.m2cs, record.bin_size.value, color = 'k', histtype='step')
                    ax.set_yscale('log')
                    ax.set_xlabel('Da')
                    ax.set_ylabel('Counts')
                    ax.set_yscale('log')

                self.ax.cla() # clear all plot objects on ax
                _plot_histogram(self.ax)

                self._preserve_ax_limits = True

        if record.ions:

            transform = blended_transform_factory(self.ax.transData, self.ax.transAxes)
            colors=itertools.cycle(list('bygrcm'))

            element_keyfunc = lambda x: x.isotope.element
            sorted_ions = sorted(record.ions, key=element_keyfunc)

            for element, ions in itertools.groupby(sorted_ions, key=element_keyfunc):

                line_color=next(colors)

                for ion in ions:

                    def _plot_suggest_line(ion):
                        y_height = ion.isotope.abundance/100
                        line = self.ax.axvline(ion.mass_to_charge, ymax=y_height, color=line_color, picker=PICKER_SENSITIVITY, label=ion.name)
                        self._ions_for_lines[line] = ion

                    def _plot_label_for_line(ion):
                        label = self.ax.annotate(ion.name, xy=(ion.mass_to_charge, 0), xycoords=transform, xytext=(ion.mass_to_charge, y_height+0.04), textcoords=transform, fontsize='small', ha='center', va='center', picker=PICKER_SENSITIVITY)
                        self._current_lines.append(line)
                        self._current_line_labels.append(label)

                    _plot_suggest_line(ion)
                    _plot_label_for_line(ion)

        if record.analyses:

            for ion, analysis in record.analyses.items():
                start, end = analysis.range
                if start == end: #TODO make safer than this
                    line = self.ax.axvline(ion.mass_to_charge, color='k', picker=PICKER_SENSITIVITY, label=ion.name, linestyle='--')
                    self._ions_for_lines[line] = ion
                else:
                    span = self.ax.axvspan(start, end, facecolor=analysis.color, alpha=0.5)
                    self._current_spans.append(span)

        self.canvas.draw()

    def on_key_press(self, event):
        key_press_handler(event, self.canvas, self.mpl_toolbar)

        if event.key == 'a':
            command = commands.AddIonsToTable([self._picked_ion], self._analyses_model)
            self._undo_stack.push(command)

        if event.key == 'r':
            command = commands.AddIonsToTable([self._picked_ion], self._analyses_model)
            self._undo_stack.push(command)
            command = commands.SelectMethod(self._picked_ion, 'Manual', self._analyses_model, self._methods_view_model)
            self._undo_stack.push(command)

            self._span_selector = SpanSelector(self.ax,self.on_span_select,'horizontal', minspan=0.0001, span_stays=True, rectprops=dict(alpha=0.5))
            QApplication.setOverrideCursor(QCursor(Qt.IBeamCursor))

    def on_pick(self, event):
        if isinstance(event.artist, Line2D):
            line=event.artist
            ion = self._ions_for_lines[line]
            new_line = self.ax.axvline(line.get_xdata()[0], color=line.get_color(), linewidth=line.get_lw()*3)

            self._current_lines.append(new_line)
            self._picked_ion = ion
            self.canvas.draw()

    def on_span_select(self,x0,x1):
        self._update_manual_range_for_ion((x0, x1))
        self._span_selector = None
        QApplication.restoreOverrideCursor()

    def _update_manual_range_for_ion(self, current_span):
        start, end = current_span
        _picked_ion = self._picked_ion
        command = commands.UpdateManualRange(_picked_ion, start, end, self._analyses_model)
        self._undo_stack.push(command)
