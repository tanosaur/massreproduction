from PyQt4 import QtCore, QtGui
import sys
# row count, column count, data method, header data
# flags (to select items or enable tiems) NOW ALSO
# index and parent for tree view.

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



class TransformNode(Node):

    def __init__(self, name, parent=None):
        super(TransformNode, self).__init__(name, parent)

    def typeInfo(self):
        return "TRANSFORM"

class CameraNode(Node):

    def __init__(self, name, parent=None):
        super(CameraNode, self).__init__(name, parent)

    def typeInfo(self):
        return "CAMERA"

class LightNode(Node):

    def __init__(self, name, parent=None):
        super(LightNode, self).__init__(name, parent)

    def typeInfo(self):
        return "LIGHT"



class SceneGraphModel(QtCore.QAbstractItemModel):

    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
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
            if section == 0:
                return "Scenegraph"
            else:
                return "Typeinfo"



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


if __name__ == '__main__':


    app = QtGui.QApplication(sys.argv)

    rootNode   = Node("Hips")
    childNode0 = TransformNode("RightPirateLeg",        rootNode)
    childNode1 = Node("RightPirateLeg_END",    childNode0)
    childNode2 = CameraNode("LeftFemur",             rootNode)
    childNode3 = Node("LeftTibia",             childNode2)
    childNode4 = Node("LeftFoot",              childNode3)
    childNode5 = LightNode("LeftFoot_END",          childNode4)

    print (rootNode)

    model = SceneGraphModel(rootNode)

    treeView = QtGui.QTreeView()
    treeView.show()

    treeView.setModel(model)


    rightPirateLeg = model.index(0, 0, QtCore.QModelIndex())


    model.insertRows(1, 5, rightPirateLeg)
    model.insertLights(1, 5 , rightPirateLeg)


    sys.exit(app.exec_())
