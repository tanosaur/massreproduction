from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4.QtGui import *
import sys

import ui_mainwindow
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


class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):

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
        # TODO make sure filenames is now a list or array with each file loaded
        commandLoad=CommandLoad(m2c, rangemethod, knownelemstr, maxchargestate, filenames, self.dataset)
        self.undoStack.push(commandLoad) #Calls the 'redo' method
        #     #see https://forum.qt.io/topic/12330/qundocommand-calls-redo-on-initialization/6

        self.stackView=QUndoView(self.undoStack, parent=self.stackView)
        self.dataset.ion_list_updated.connect(self.on_ionlist_updated_add_nodes)
        self.dataset.range_table_updated.connect(self.on_range_table_updated)

        self.foo=rangedFrame(self.dataset,3000,parent=self.rangedFrame)
        self.ionlistData=None

    @pyqtSlot(list)
    def on_range_table_updated(self,ionlist):
        self.tableNode=Node('RangeList')

        for line in ionlist:
            for x in line:
                Node(x,self.tableNode)

        self.rangelistData=ionlistModel(self.tableNode)
        self.rangedTable.setModel(self.rangelistData)
        print(self.tableNode)

    @pyqtSlot(np.ndarray,list)
    def on_ionlist_updated_add_nodes(self, ionstringlist, suggestedtitle):
        self.rootNode=Node('IonList')

        for line in np.arange(len(ionstringlist)):
            Node(ionstringlist[line],self.rootNode)

        self.ionlistData=ionlistModel(self.rootNode)
        self.ionlistTree.setModel(self.ionlistData)
        self.ionlistTree.setSelectionMode(3)
        print(self.rootNode)

    @pyqtSignature("") # Must be included even if ""
    def on_addionsButton_clicked(self):
        # Retrieve highlighted labels
        # Add the name and suggest m2c to the table
        qmodel_indices=self.ionlistTree.selectedIndexes()
        refs=[self.ionlistData.data(x, role=QtCore.Qt.DisplayRole) for x in qmodel_indices]
        commandAddIons=CommandAddIonsToTable(refs, self.dataset)
        self.undoStack.push(commandAddIons)

    @pyqtSignature("") # Must be included even if ""
    def on_actionLoad_triggered(self):
        loadDlg=load.loadDialog(self.dataset)
        loadDlg.loaded.connect(self.on_loaded) #TODO is this needed?
        loadDlg.setModal(True) #see how this actually affects things later
        loadDlg.exec_()

    # @pyqtSignature("") # Must be included even if ""
    # def on_actionHistory_triggered(self):
    #     histDlg=histWidget(self, self.undoStack)
    #     histDlg.setModal(True) #see how this actually affects things later
    #     histDlg.exec_() #TODO implement history view as new window or side window

    @pyqtSignature("") # Must be included even if ""
    def on_actionSave_As_triggered(self):
        print("save as triggered")

    @pyqtSignature("") # Must be included even if ""
    def on_actionSave_triggered(self):
        print("save triggered")

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
        commandSuggest=CommandSuggest(
            str(self.knownelementsLineEdit.text()),
            abs(int(str(self.maxchargestateLineEdit.text()))),
            self.dataset
        )
        self.undoStack.push(commandSuggest)

    def updateUi(self):
        enable=not self.knownelementsLineEdit.text().isEmpty() #TODO #add suggestLineEdit test as well
        # Enables the 'Suggest' button
        #TODO wtf? the error message
        self.suggestButton.setEnabled(enable) #TODO initially disable this and also load button

    @pyqtSignature("QString")
    def on_knownelementsLineEdit_textEdited(self,text):
        self.updateUi()

class rangetableModel(QAbstractTableModel):
    def __init__(self, name, parent=None):
        self.name=name

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        return 5

    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name()
            if index.column() == 1:
                return 'hihi'

        if role == QtCore.Qt.DecorationRole:
            pass

    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0 and orientation==Qt.Horizontal:
                return "Ion"

    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():

            if role == QtCore.Qt.EditRole:

                node = index.internalPointer()
                node.setName(value)

                return True
        return False

    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    """INPUTS: int, int, QModelIndex"""
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):

        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)

        for row in range(rows):

            childCount = parentNode.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)

        self.endInsertRows()

        return success

    """INPUTS: int, int, QModelIndex"""
    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)

        self.beginInsertColumns(parent, position, position + columns - 1)

        for row in range(rows):

            childCount = parentNode.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)

        self.endInsertColumns()

        return success

class Node(object):

    def __init__(self, name, parent=None):

        self._name = name # Given
        self._children = [] # Received children
        self._parent = parent # Input parent

        if parent is not None:
            parent.addChild(self) # Custom method

    def typeInfo(self):
        return "NODE"

    def addChild(self, child):
        self._children.append(child) # Adds given child to children list

    def insertChild(self, position, child):

        if position < 0 or position > len(self._children):
            return False

        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):

        if position < 0 or position > len(self._children):
            return False

        child = self._children.pop(position)
        child._parent = None

        return True


    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    # Just to visualise our exercise
    def log(self, tabLevel=-1): # Increase the tab level before recursing any children
    # And then decrease the tab level

        output     = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "\t" # Increase tab count at output text

        output += "|------" + self._name + "\n" # Add name of current node and line break

        for child in self._children:
            output += child.log(tabLevel)

        tabLevel -= 1
        output += "\n"

        return output

    def __repr__(self):
        return self.log()

class ionlistModel(QAbstractItemModel):
    def __init__(self, root, parent=None):
        super(ionlistModel, self).__init__(parent)
        self._rootNode = root

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        return 1

    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name()
            if index.column() == 1:
                return 'hihi'

        if role == QtCore.Qt.DecorationRole:
            pass



    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():

            if role == QtCore.Qt.EditRole:

                node = index.internalPointer()
                node.setName(value)

                return True
        return False


    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0 and orientation==Qt.Horizontal:
                return "Ion"


    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    """INPUTS: QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return the parent of the node with the given QModelIndex"""
    def parent(self, index):

        node = self.getNode(index)
        parentNode = node.parent() # Return parent of the given index

        if parentNode == self._rootNode: # Check parent node is the root node the Tree model holds
            return QtCore.QModelIndex() # Wrap it around QModelIndex

        # If not it's a child -> create model # Only in 1 column [0]
        return self.createIndex(parentNode.row(), 0, parentNode) # Return it

    """INPUTS: int, int, QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return a QModelIndex that corresponds to the given row, column and parent node"""
    def index(self, row, column, parent):

        parentNode = self.getNode(parent)

        childItem = parentNode.child(row)

        if childItem: # Wrap in Q Model index and return
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex() # Return empty index

    """CUSTOM"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._rootNode

    """INPUTS: int, int, QModelIndex"""
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):

        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)

        for row in range(rows):

            childCount = parentNode.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)

        self.endInsertRows()

        return success

    """INPUTS: int, int, QModelIndex"""
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):

        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)

        for row in range(rows):
            success = parentNode.removeChild(position)

        self.endRemoveRows()

        return success

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
        # self.canvas.mpl_connect('pick_event', self.onpick)
        # self.canvas.mpl_connect('button_press_event', self.onclick)

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

        self.ss=SpanSelector(self.ax,self.onselect,'horizontal', minspan=0.0001)
        #TODO minspan was a fix for any click creating a small span, fix later by taking hold on SpanSelector off
        #or set span_stays=False



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

    @pyqtSlot(np.ndarray, np.ndarray)
    def on_suggest(self,m2cs,names):
        self.ax.lines=[] #These are necessary to clear the lines and labels for every undo/redo.
        self.ax.texts=[]

        for l in np.arange(len(m2cs)):
            linecolor=next(self.colors) #fix this...!
            self.ax.axvline(m2cs[l], color=linecolor)
            self.ax.text(m2cs[l],100,names[l],fontsize=10) #TODO TREAT OVERLAPPING SOMEHOW
            # #TODO keep labels centered on line (x position), and at top relative to window size! (y position)

        self.fig.canvas.draw()

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
