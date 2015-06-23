from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

import ui_mainwindow
import load

import numpy as np
from itertools import cycle

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
from matplotlib.backends import qt_compat
from matplotlib.backend_bases import key_press_handler
from matplotlib.widgets import SpanSelector

import matplotlib
# matplotlib.rcParams['keymap.pan'] = u'super+p'

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
    suggest=pyqtSignal(np.ndarray, np.ndarray) #passing array

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.MC=''
        self.LEN=''

    @pyqtSlot(np.ndarray,int)
    def on_loaded(self,m2c,length):
        self.MC=m2c #use set functions and also learn how to initialise
        self.LEN=length
        self.plotWidget=workingFrame(self.MC,3000,parent=self.workingFrame)
        self.foo=rangedFrame(self.MC,3000,parent=self.rangedFrame)

    @pyqtSignature("") # Must be included even if ""
    def on_actionLoad_triggered(self):
        loadDlg=load.loadDialog()
        loadDlg.loaded.connect(self.on_loaded)
        loadDlg.setModal(True) #see how this actually affects things later
        loadDlg.exec_()

    @pyqtSignature("") # Must be included even if ""
    def on_suggestButton_clicked(self):
        element=str(self.knownelementsLineEdit.text())
        self.suggest.connect(self.plotWidget.on_suggest)
        if element == 'Al':
            elmasses=np.array([25.986892,26.981538]) # stable for more than 7s
            elnames=np.array(['Al 26', 'Al 27'])
            self.suggest.emit(elmasses, elnames)

    def updateUi(self):
        enable=not self.knownelementsLineEdit.text().isEmpty() #TODO #add suggestLineEdit test as well
        # Enables the 'Suggest' button
        self.suggestButton.setEnabled(enable) #TODO initially disable this and also load button

    @pyqtSignature("QString")
    def on_knownelementsLineEdit_textEdited(self,text):
        self.updateUi()


class workingFrame(QMainWindow):

    def __init__(self, data, bins, parent=None):

        super(workingFrame, self).__init__(parent)

        self.fig=Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()

        self.mpl_toolbar = NavigationToolbar(self.canvas, parent)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        vbox.addWidget(self.mpl_toolbar)
        parent.setLayout(vbox)

        self.ax=self.fig.add_subplot(111)
        self.ax.hold(False)
        self.ax.hist(data,bins,histtype='step')
        self.ax.set_yscale('log')

        self.colors=cycle(list('rybmc'))
        self.ss=SpanSelector(self.ax,self.onselect,'horizontal')
        self.canvas.draw()

    def onselect(self,x0,x1):
        self.ax.axvspan(x0,x1, facecolor=next(self.colors), alpha=0.5)
        print(x0,x1)
        self.fig.canvas.draw_idle() #keeps the selection drawn on

    def on_key_press(self, event):
        print('you pressed', event.key)
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.canvas, self.mpl_toolbar)

    @pyqtSlot(np.ndarray, np.ndarray)
    def on_suggest(self,elmasses, elnames):
        #could remove additional entries but need to think more deeply about MVC structure
        #and saving data
        self.ax.hold(False)
        linecolor=next(self.colors)
        for i in np.arange(len(elmasses)):
            self.ax.axvline(elmasses[i], color=linecolor, label=elnames[i])
            self.fig.canvas.draw_idle()
        self.ax.legend()

class rangedFrame(QMainWindow):

    def __init__(self, data, bins, parent=None):

        super(rangedFrame, self).__init__(parent)

        self.fig=Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        parent.setLayout(vbox)

        ax=self.fig.add_subplot(111)
        ax.hold(False)
        ax.hist(data,bins,histtype='step')
        self.canvas.draw()

app=QApplication(sys.argv)
form=MainWindow()
form.show()
# s=MainWindow.rangedFrame.size()
# MainWindow.plotWidget.setGeometry(1,1, s.width()-2, s.height()-2)
app.exec_()
