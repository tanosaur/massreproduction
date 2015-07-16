from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

import ui_mainwindow2
import ui_historywidget
import load
from commands import *
from dataset2 import DataSet

import numpy as np
from itertools import cycle

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
from matplotlib.backends import qt_compat
from matplotlib.backend_bases import key_press_handler
from matplotlib.widgets import SpanSelector
import matplotlib #TODO take this out if possible

import aptread.aptload
# matplotlib.rcParams['keymap.pan'] = u'super+p'

# class histWidget(QWidget, ui_historywidget.Ui_historyWidget):
#     def __init__(self, undostack, parent=None):
#         super(histWidget, self).__init__(parent)
#
#         self.view=QUndoView(self, undoStack, parent=histWidget)

# class stackView(QWidget):
#     def __init__(self, stack, parent=None):
#         super(stackView, self).__init__(parent)
#         self.viewHist=QUndoView(stack)

class MainWindow(QMainWindow, ui_mainwindow2.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.dataset = DataSet(self)
        filenames='/Users/claratan/OneDrive/GUI/data/R04.pos' #TODO change so that
            #multiple files added append to array
            #combine the data, then set as m2c and configure length!
        m2c=aptread.aptload.APData(filenames).pos.mc
        rangemethod=2
        knownelemstr='H'
        maxchargestate=2

        self.plotWidget=workingFrame(self.dataset,3000,parent=self.workingFrame)

        # TODO configure filename separation for print (e.g. each element of array separated by comma, convert to string)
        self.undoStack=QUndoStack(self)
        commandLoad=CommandLoad(m2c, rangemethod, knownelemstr, maxchargestate, 'Load: (%s)' %filenames, self.dataset)
        self.undoStack.push(commandLoad) #Calls the 'redo' method
            #see https://forum.qt.io/topic/12330/qundocommand-calls-redo-on-initialization/6

        self.stackView=QUndoView(self.undoStack, parent=self.stackView)
        # stackView(self.undoStack)
        self.foo=rangedFrame(self.dataset,3000,parent=self.rangedFrame)

    @pyqtSignature("") # Must be included even if ""
    def on_actionLoad_triggered(self):
        loadDlg=load.loadDialog(self.dataset)
        loadDlg.loaded.connect(self.on_loaded) #TODO is this needed?
        loadDlg.setModal(True) #see how this actually affects things later
        loadDlg.exec_()

    @pyqtSignature("") # Must be included even if ""
    def on_actionHistory_triggered(self):
        histDlg=histWidget(self, self.undoStack)
        histDlg.setModal(True) #see how this actually affects things later
        histDlg.exec_()

    @pyqtSignature("") # Must be included even if ""
    def on_actionUndo_triggered(self):
        print("undo triggered")
        self.undoStack.undo()

    @pyqtSignature("") # Must be included even if ""
    def on_actionRedo_triggered(self):
        print("redo triggered")
        self.undoStack.redo()

    @pyqtSignature("") # Must be included even if ""
    def on_suggestButton_clicked(self):
        self.dataset.load_suggest(str(self.knownelementsLineEdit.text()), int(str(self.maxchargestateLineEdit.text())))
        commandSuggest=CommandSuggest('Suggest ions', self.dataset)
        self.undoStack.push(commandSuggest)

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
        # self.ax.hist(data.m2c,bins,histtype='step')
        # self.ax.set_yscale('log')
        self.bins = bins
        self.lines=0

        data.m2c_updated.connect(self.on_dataset_m2c_updated)
        data.suggest.connect(self.on_suggest)
        data.suggestUndo.connect(self.on_suggestUndo)
            #TODO think: data will not need to be passed in if signals aren't there...

        self.ss=SpanSelector(self.ax,self.onselect,'horizontal')
        # self.canvas.draw()

    @pyqtSlot(np.ndarray)
    def on_dataset_m2c_updated(self, m2c):
        print("model update loopback")
        if not m2c.any():
            self.ax.cla()
        else:
            self.colors=cycle(list('rybmc'))
            self.ax.hist(m2c, self.bins, histtype='step')
            self.ax.set_yscale('log')

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

    @pyqtSlot(list,int)
    def on_suggest(self,elements,mcs):
        self.ax.hold(False)
        self.lines=0

        _lookup=dict(Al=[(27,26.98,100)],Cr=[(50,49.95,4.3),(52,51.94,83.8),(53,52.94,9.5),(54,53.94,2.4)],H=[(1,1.008,99.985),(2,2.014,0.015)])
        for i in np.arange(len(elements)):
            linecolor=next(self.colors)
            records=_lookup[elements[i]]
            name=np.empty(len(records)*mcs,dtype=object)
            m2c=np.empty(len(records)*mcs)

            for k in np.arange(mcs)+1:
                for j in np.arange(len(records)):
                    name[j+((k-1)*len(records))]=str(records[j][0])+elements[i]+'+'+str(k) #concat with element name and charge state
                    m2c[j+((k-1)*len(records))]=records[j][1]/k

            for l in np.arange(len(records*mcs)):
                self.ax.axvline(m2c[l], color=linecolor)
                self.ax.text(m2c[l],100,name[l],fontsize=10) #TODO TREAT OVERLAPPING SOMEHOW
                # #TODO keep labels centered on line (x position), and at top relative to window size! (y position)
                self.fig.canvas.draw_idle()
                # # print(self.ax.get_ylim())
                self.lines=self.lines+1

    @pyqtSlot()
    def on_suggestUndo(self):
        for m in np.arange(self.lines):
            self.ax.lines.pop(0)
        self.canvas.draw()


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
        ax.hist(data.m2c,bins,histtype='step')
        ax.set_yscale('log')
        self.canvas.draw()

app=QApplication(sys.argv)
form=MainWindow()
form.show()
# s=MainWindow.rangedFrame.size()
# MainWindow.plotWidget.setGeometry(1,1, s.width()-2, s.height()-2)
app.exec_()
