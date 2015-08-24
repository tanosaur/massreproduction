from PyQt4 import QtCore
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
        self._root_node = root

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def rowCount(self, parent):
        if not parent.isValid():
            parent_node = self._root_node
        else:
            parent_node = parent.internalPointer()

        return parent_node.childCount()

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        if not parent.isValid():
            parent_node = self._root_node
        else:
            parent_node = parent.internalPointer()

        return parent_node.columnCount()

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
        parent_node = node.parent() # Return parent of the given index

        if parent_node == self._root_node: # Check parent node is the root node the Tree model holds
            return QtCore.QModelIndex() # Wrap it around QModelIndex

        # If not it's a child -> create model # Only in 1 column [0]
        return self.createIndex(parent_node.row(), 0, parent_node) # Return it

    """INPUTS: int, int, QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return a QModelIndex that corresponds to the given row, column and parent node"""
    def index(self, row, column, parent):

        parent_node = self.getNode(parent)

        childItem = parent_node.child(row)


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

        return self._root_node


    """INPUTS: int, int, QModelIndex"""
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):

        parent_node = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)

        for row in range(rows):

            childCount = parent_node.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parent_node.insertChild(position, childNode)

        self.endInsertRows()

        return success

    def insertLights(self, position, rows, parent=QtCore.QModelIndex()):

        parent_node = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)

        for row in range(rows):

            childCount = parent_node.childCount()
            childNode = LightNode("light" + str(childCount))
            success = parent_node.insertChild(position, childNode)

        self.endInsertRows()

        return success

    """INPUTS: int, int, QModelIndex"""
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):

        parent_node = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)

        for row in range(rows):
            success = parent_node.removeChild(position)

        self.endRemoveRows()

        return success
