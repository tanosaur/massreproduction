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

        self._ions_for_lines = {}
        self._picked_ion = None

        self._old_m2cs = None
        self._old_bin_size = None

        self._current_lines = []
        self._current_line_labels = []
        self._current_spans = []

        self._analyses_model = analyses_model
        self._methods_view_model = methods_view_model
        self._undo_stack = undo_stack

        self._preserve_ax_limits = False


    @pyqtSlot(WorkingPlotRecord)
    def on_updated(self, record):
        def _(plot_object):
            plot_object = list(filter(None, plot_object))
            emptied_plot_object = [_object.remove() for _object in plot_object]
            return emptied_plot_object

        if self._current_spans:
            self._current_spans = _(self._current_spans)
        if self._current_lines:
            self._current_lines = _(self._current_lines)
            self._current_line_labels = _(self._current_line_labels)

        if record.m2cs:
            if self._preserve_ax_limits:
                cur_xlim = self.ax.get_xlim()
                cur_ylim = self.ax.get_ylim()
                self.ax.set_xlim(cur_xlim)
                self.ax.set_ylim(cur_ylim)

            if self._old_m2cs != record.m2cs or self._old_bin_size != record.bin_size.value:
                self._old_m2cs = record.m2cs
                self._old_bin_size = record.bin_size.value

                self.ax.cla()
                self.ax.hist(record.m2cs, record.bin_size.value, color = 'k', histtype='step')
                self.ax.set_yscale('log')
                self.ax.set_xlabel('Da')
                self.ax.set_ylabel('Counts')
                self.ax.set_yscale('log')
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
                    line = self.ax.axvline(ion.mass_to_charge, ymax=y_height, color=line_color, picker=PICKER_SENSITIVITY, label=ion.name)
                    self._ions_for_lines[line] = ion
                    label = self.ax.annotate(ion.name, xy=(ion.mass_to_charge, 0), xycoords=trans, xytext=(ion.mass_to_charge, y_height+0.04), textcoords=trans, fontsize='small', ha='center', va='center', picker=PICKER_SENSITIVITY)
                    self._current_lines.append(line)
                    self._current_line_labels.append(label)

        if record.analyses:

            for ion, analysis in record.analyses.items():
                start, end = analysis.range
                if start == end: #TODO make safer than this
                    line = self.ax.axvline(ion.mass_to_charge, color='k', picker=PICKER_SENSITIVITY, label=ion.name)
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
        if event.key == 'm':
            pass
        if event.key == 's':
            command = commands.SelectMethod(self._picked_ion, 'Manual', self._analyses_model, self._methods_view_model)
            self._undo_stack.push(command)
            self._span_selector = SpanSelector(self.ax,self.on_span_select,'horizontal', minspan=0.0001, span_stays=True, rectprops=dict(alpha=0.5))
            QApplication.setOverrideCursor(QCursor(Qt.IBeamCursor))
        if event.key == 'c':
            self._update_manual_range_for_ion(self._current_span)
            self._span_selector = None
            QApplication.restoreOverrideCursor()

    def on_pick(self, event):

        def _get_line_IDs(lines):
            for line in lines:
                print(self._ions_for_lines[line].name)

        def _thicken_selected_line(line):
            new_line = self.ax.axvline(line.get_xdata()[0], color=line.get_color(), linewidth=line.get_lw()*3)
            self._ions_for_lines[new_line] = ion
            self._current_lines.append(new_line)
            self._current_lines.remove(line)
            line.remove()
            _get_line_IDs(self._current_lines)

        def _clear_selected_line(line):
            print(line.get_lw())
            _get_line_IDs([line])
            new_line = self.ax.axvline(line.get_xdata()[0], color=line.get_color(), linewidth=1)
            # self._current_lines.remove(line)
            # line.remove()
            self._ions_for_lines[new_line] = ion
            # self._current_lines.append(new_line)
            _get_line_IDs(self._current_lines)

        def _clear_previous_selected_line():
            self._lines_for_ions = {v: k for k, v in self._ions_for_lines.items()}
            previous_selected_line = self._lines_for_ions[self._picked_ion]
            _clear_selected_line(previous_selected_line)

        if isinstance(event.artist, Line2D):
            line=event.artist
            ion = self._ions_for_lines[line]
<<<<<<< HEAD
            if ion == self._picked_ion:
                print('same ion picked')
                _clear_selected_line(line)
                self._picked_ion = None
            elif self._picked_ion == None:
                print('new ion picked')
                _thicken_selected_line(line)
                self._picked_ion = ion
            else:
                print('different ion picked')
                _clear_previous_selected_line()
                _thicken_selected_line(line)
                self._picked_ion = ion

=======
            new_line = self.ax.axvline(line.get_xdata()[0], color=line.get_color(), linewidth=line.get_lw()*3)
            self._current_lines.append(new_line)
            self._picked_ion = ion
>>>>>>> 57a1aea... before testing
            self.canvas.draw()

    def on_span_select(self,x0,x1):
        self._current_span = (x0, x1)

    def _update_manual_range_for_ion(self, current_span):
        start, end = current_span
        _picked_ion = self._picked_ion
        command = commands.UpdateManualRange(_picked_ion, start, end, self._analyses_model)
        self._undo_stack.push(command)
