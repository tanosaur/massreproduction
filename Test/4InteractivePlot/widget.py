from PyQt4.QtCore import *
from PyQt4.QtGui import *
import matplotlib
import sys
# specify the use of PyQT4
matplotlib.rcParams['backend.qt4'] = "PyQt4"
# import the figure canvas for interfacing with the backend
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas # import 3D plotting
from matplotlib.figure import Figure

class workingWidget(FigureCanvas):
	def __init__(self, data, binsize, parent=None):
		self.figure=Figure(facecolor=(0,0,0))
		super(widget, self).__init__(self.figure)
		self.setParent(parent)
		self._data=data
		binsize=bins #temporary
		self._bins=bins

		ax=self.figure.add_subplot(111)
		ax.hold(False)
		ax.hist(data, bins, histtype='step')
