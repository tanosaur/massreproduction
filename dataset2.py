import unittest
import numpy as np
from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4 import QtCore, QtGui

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

class IonListModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None):
        super(IonListModel, self).__init__(parent)
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
            if section == 0 and orientation==QtCore.Qt.Horizontal:
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

class Node2(object):

    def __init__(self, name, method, start, end, parent=None):

        self._name = name # Given
        self._method= method
        self._start=start
        self._end=end
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

    def method(self):
        return self._method

    def setMethod(self, method):
        self._method = method

    def start(self):
        return self._start

    def setStart(self, start):
        self._start = start

    def end(self):
        return self._end

    def setEnd(self, end):
        self._end = end


    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def columnCount(self):
        return 4

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    # # Just to visualise our exercise
    # def log(self, tabLevel=-1): # Increase the tab level before recursing any children
    # # And then decrease the tab level
    #
    #     output     = ""
    #     tabLevel += 1
    #
    #     for i in range(tabLevel):
    #         output += "\t" # Increase tab count at output text
    #
    #     output += "|------" + self._name + "\n" # Add name of current node and line break
    #
    #     for child in self._children:
    #         output += child.log(tabLevel)
    #
    #     tabLevel -= 1
    #     output += "\n"
    #
    #     return output

    # def __repr__(self):
    #     return self.log()

class RangeTableModel(QtCore.QAbstractItemModel):

    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(RangeTableModel, self).__init__(parent)
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
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.columnCount()

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
                return node.method()
            if index.column() == 2:
                return node.start()
            if index.column() == 3:
                return node.end()

        if role == QtCore.Qt.DecorationRole:
            pass



    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():

            if role == QtCore.Qt.EditRole and index.column() == 1:

                node = index.internalPointer()
                node.setMethod(value)

                return True
        return False


    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0 and orientation==QtCore.Qt.Horizontal:
                return "Ion"
            if section == 1 and orientation==QtCore.Qt.Horizontal:
                return "Method"
            if section == 2 and orientation==QtCore.Qt.Horizontal:
                return "Start"
            if section == 3 and orientation==QtCore.Qt.Horizontal:
                return "End"

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

    def insertLights(self, position, rows, parent=QtCore.QModelIndex()):

        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)

        for row in range(rows):

            childCount = parentNode.childCount()
            childNode = LightNode("light" + str(childCount))
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

class DataSet(QObject):
    m2c_updated = pyqtSignal(np.ndarray)
    suggest=pyqtSignal(np.ndarray, np.ndarray)
    ion_list_updated=pyqtSignal(np.ndarray, list)
    range_table_updated=pyqtSignal(list)

    def __init__(self, parent=None):
        super(DataSet, self).__init__(parent)
        self.m2c=[]
        self.method=None
        self.maxchargestate=None
        self.knownelems=None

        self.names=[]
        self.m2cs=[]
        self.allnames=np.array([])
        self.suggestedelements=[]

        self.ionsintable=[]

    def set_ionsintable(self,loadionlist):
        self.ionsintable.append(loadionlist)

    def load(self, data, method, knownelemstring, maxchargestate):
        self.m2c=data
        self.method=method
        self.maxchargestate=abs(maxchargestate)
        knownelemstring=str(knownelemstring) #TODO WHY WAS THIS NECESSARY
        self.knownelems=knownelemstring.split(',')

    def load_suggest(self,suggestelemstring,maxchargestate):
        self.suggestedelements=suggestelemstring.split(',')

        _lookup={
            "Al": [(27,26.98,100)],
            "Cr": [(50,49.95,4.3),(52,51.94,83.8),(53,52.94,9.5),(54,53.94,2.4)],
            "H":  [(1,1.008,99.985),(2,2.014,0.015)]
        }

        for element in self.suggestedelements:
            records=_lookup[element]
            names=np.empty(len(records)*maxchargestate,dtype=object)
            m2cs=np.empty(len(records)*maxchargestate)
            abundance=np.empty(len(records)*maxchargestate)

        #Thinking that charge states will be implemented as next row (isotopes with same charge state on same row)
        #TODO investigate charge states vs. Peter's code

            for k in np.arange(maxchargestate)+1:
                for j in np.arange(len(records)):
                    names[j+((k-1)*len(records))]=str(records[j][0])+element+'+'+str(k) #concat with element name and charge state
                    m2cs[j+((k-1)*len(records))]=records[j][1]/k
                    abundance[j+((k-1)*len(records))]=records[j][2]

        self.names=names
        self.m2cs=m2cs
        self.allnames=np.append(self.allnames, self.names)


class TestDataSet(unittest.TestCase):

    def dataset_with_data(self):
        d = DataSet()
        d.load(np.array([1, 2]), 2)
        return d

    def test_empty_dataset(self):
        d = DataSet()
        self.assertTrue(np.array_equal(d.m2c, np.array([])))

    def test_load(self):
        d = self.dataset_with_data()
        self.assertTrue(np.array_equal(d.m2c, np.array([1,2])))

    def test_undo_on_empty_dataset(self):
        # Arrange
        d = DataSet()
        d.undo() # Act
        self.assertTrue(np.array_equal(d.m2c, np.array([]))) # Assert

    def test_undo_on_changed_dataset(self):
        d=DataSet()
        theonebeforechanged=d.m2c
        d.load(np.array([1, 2]), 2)
        d.undo() # Act
        self.assertTrue(np.array_equal(d.m2c,theonebeforechanged)) # Assert

    def test_redo_on_full_dataset(self):
        pass

    def test_redo_on_changed_dataset(self):
        d = self.dataset_with_data()
        original_d = d.m2c
        d.undo()
        d.redo()
        self.assertTrue(np.array_equal(d.m2c, original_d))

    def test_undo_emits_m2c_updated_signal(self):
        d = DataSet()
        d.load(np.array([1, 2]), 2)
        self.m2c_update = False
        def _on_m2c_updated(m2c):
            self.m2c_update = m2c
        d.m2c_updated.connect(_on_m2c_updated)
        d.undo()
        self.assertTrue(np.array_equal(self.m2c_update, d.m2c))

#    def test_undo_emits_m2c_updated_signal(self):
#        d = DataSet()
#        d.load(np.array([1, 2]), 2)
#        updated = (False, True).__iter__()
#        d.m2c_updated.connect(updated.__next__)
#        d.undo()
#        self.assertTrue(updated.__next__())

if __name__ == '__main__':
    # unittest.main()
    make=DataSet()
    make.load(np.array([]), 2, 1, 'Al,Cr', 3)
