# /----------------\
# | Name | Age     |
# +------+---------v+
# | Scott| Ancient |
# | Clara| Moulding|
# \----------------/
#
# X
# Y
#     Z
# B
#
#
#
#
#
# QtTableView
#   QtModel
#    + headers => QtArray{QtString}
#    + data => QtArray row
#                 QtArray column
#                     QtString "Scott" or "Moulding"
#
#
people = [["Scott", "Ancient"], ["Clara", "Moulding"]]

# class MyViewModel:
#     def __init__(self, people):
#         self.people = people
#
#     def headers(self):
#         array = QtArray()
#         array.append("Name")
#         array.append("Age")
#         return array
#
#     def data(self, row, column):
#         return QtString(people[row][column])
#
#     def index(self, row, column, parent):
#         pass

class MyViewModel:
    def __init__(self, people):
        self.people = people

    def headers(self):
        return ['Name','Age']

    def data(self, row, column):
        return people[row][column]

    def index(self, row, column, parent):
        pass

#
#
#
# rows = [
#     [String, String],
#     [String, String]
# ]
# row_1 = rows[0]
# row_1_column_1 = rows[0][0] # Outermost is row, innermost is column

from PyQt4 import QtCore

class Node(object):

    def __init__(self, name, parent=None, abundance=None):

        self._name = name # Given
        self._abundance = abundance
        self._children = [] # Received children
        self._parent = parent # Input parent

        if parent is not None:
            parent.addChild(self) # Custom method

    def typeInfo(self):
        return "NODE"

    def addChild(self, child):
        self._children.append(child) # Adds given child to children list

    def name(self):
        return self._name

    def abundance(self):
        return self._abundance

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

# root_node
#   Node name = Scott age = Timelies
#   Node name Clara age = annyoung
#
# initial_index = QtModelIndex(row=0, column=0, pointer=None) # initialiser, creates a QIndex
#
# model=MyViewModel(people)
#
# model.index(row=0, column=0, parent=initial_index) ->>
#     Index(row=0, column=0, pointer=ScottNode)


class IonListModel(QtCore.QAbstractItemModel): # QAbstractItemModel used for Qt tree views
    def __init__(self, suggested_ions):
        super(IonListModel, self).__init__(None)
        self._suggestion_ions = suggested_ions
        self._root_node = Node('IonList')

        for element, ions in suggested_ions.items():
            element_node= Node(element, self._root_node)
            for ion in ions:
                label, m2c, abundance = ion
                Node(label,element_node,str(abundance))


    def index(self, row, column, parent): #int, int, QModelIndex
        # print("Index: %s %s %s" % (row, column, parent))

        parentNode = self._getNode(parent)

        childItem = parentNode.child(row)

        if childItem: # Wrap in Q Model index and return
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex() # Return empty index

    def parent(self, index):

        node = self._getNode(index)
        parent_node = node.parent() # Return parent of the given index

        if parent_node == self._root_node: # Check if parent node is the root node
            return QtCore.QModelIndex() # Return empty index

        # If not, it's a child -> create model # Only in 1 column [0]
        return self.createIndex(parent_node.row(), 0, parent_node) # Return it

    def rowCount(self, parent):
        if not parent.isValid():
            parent_node = self._root_node
        else:
            parent_node = parent.internalPointer()

        return parent_node.childCount()

        # TODO Scott - how is childCount() giving the row when there are two items in each row?

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return None
            # None is interpreted as an invalid QVariant
            # An invalid QVariant must be returned (not 0)

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return node.name()
            if index.column() == 1 and node.abundance():
                return node.abundance()


    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0 and orientation==QtCore.Qt.Horizontal:
                return "Ion"
            if section == 1 and orientation==QtCore.Qt.Horizontal:
                return "Abundance (%)"

    def _getNode(self, index):
        if index.isValid():
            node = index.internalPointer() # Item index was pointing to
            if node:
                return node

        return self._root_node
