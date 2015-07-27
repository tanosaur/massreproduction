import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import aptread.aptload
from itertools import cycle

class workingWidget(QWidget):
    def __init__(self, data, bins, parent=None):
        super(workingWidget, self).__init__(parent)
        self._data=data
        self._bins=bins

        # a figure instance to plot on
        self.figure = Figure()

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

        self.colors=cycle(list('rybmc'))
        # create an axis
        self.ax = self.figure.add_subplot(111)

        # discards the old graph
        self.ax.hold(False)

        # plot data
        self.ax.hist(data, bins, histtype='step')

        self.ss=SpanSelector(self.ax,self.onselect, 'horizontal')
        # refresh canvas
        self.canvas.draw()


    def onselect(self,x0,x1):
        self.ax.axvspan(x0,x1, facecolor=next(self.colors), alpha=0.5)
        print(x0,x1)
        self.figure.canvas.draw_idle() #keeps the selection drawn on



if __name__ == '__main__':


    posFilename='/Users/claratan/OneDrive/GUI/data/R04.pos'

    class NPM():

        def __init__(self, data, parent=None):
            self.XYZ=data.pos.xyz
            self.MC=data.pos.mc
            self.LEN=len(data.pos)

    RM=NPM(aptread.aptload.APData(posFilename))
    xyz=RM.XYZ
    mc=RM.MC

    app = QApplication(sys.argv)

    main = workingWidget(RM.MC, 3000)
    main.show()

    sys.exit(app.exec_())
