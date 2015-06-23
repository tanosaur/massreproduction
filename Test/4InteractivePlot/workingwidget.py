import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import aptread.aptload

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

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.hist(data, bins, histtype='step')

        # refresh canvas
        self.canvas.draw()


if __name__ == '__main__':


    posFilename='/Users/claratan/OneDrive/Thesis/GUI/Step 3 Loadsave data/data/R04.pos'

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
