from PyQt4 import QtGui, QtCore
import sys




# Must subclass any abstract model

class PaletteListModel(QtCore.QAbstractListModel):

    def __init__(self, colors=[], parent=None):
        QtCore.QAbstractListModel.__init__(self,parent) #The super class constructor, passing parent argument.
        self.__colors=colors # Store input color list in a private list

    #EVERY MODEL MUST IMPLEMENT 2 METHODS AT MIN IN PYQT
    # 'data' and 'rowcount'
    # Or you'll get empty windows even if model-view set up and working.

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString("Palette")
            else:
                return QtCore.QString("Color %1").arg(section)


    def rowCount(self, parent): # Can ignore the parent parameter if working on list, not tree.
        """Tell view how many items model contains.
        View needs to know so it can ask for the data within the
        rowcount range."""
        return len(self.__colors)


    def data(self, index, role):
        """View will call data for every row which the row count method returns"""

        if role == QtCore.Qt.EditRole:
            return self.__colors[index.row()].name()


        if role == QtCore.Qt.ToolTipRole:
            return "Hex code: " + self.__colors[index.row()].name()


        if role == QtCore.Qt.DecorationRole:

            row = index.row()
            value = self.__colors[row]

            pixmap = QtGui.QPixmap(26, 26)
            pixmap.fill(value)

            icon = QtGui.QIcon(pixmap)

            return icon


        if role == QtCore.Qt.DisplayRole:

            row = index.row()
            value = self.__colors[row]

            return value.name()



    def flags(self, index): #Don't actually care about index
        """Flags method called by view to check states.
        E.g. here, Return that the item is indeed editable"""
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        # Since we are overwriting the old flags method from the inherited QAbstractListModel
        # we actually have to supply more flags (?)


    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole: #also the default role (input ^)

            row = index.row()
            color = QtGui.QColor(value) #value hopefully contains hex code for color

            if color.isValid(): #if so
                self.__colors[row] = color
                self.dataChanged.emit(index, index) # !! Emit signal now if the data has been changed
                # Requires 2 inputs, but ours is only a list (not rows and cols) so just pass index to both
                return True
        return False


    #=====================================================#
    #INSERTING & REMOVING
    #=====================================================#

    # Note we are still OK to ignore the parent parameter
    # because we are not working in a hierarchial tree manner yet.

    # (Parent is an empty qmodelindex)

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        # MUST ^
        for i in range(rows):
            self.__colors.insert(position, QtGui.QColor("#000000"))
            # Note insert keeps pushing the 'position' downwards by nature
        self.endInsertRows()
        # MUST ^
        return True



    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            value = self.__colors[position]
            self.__colors.remove(value)

        self.endRemoveRows()
        return True






if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")


    #ALL OF OUR VIEWS
    listView = QtGui.QListView()
    listView.show()

    treeView = QtGui.QTreeView()
    treeView.show()

    comboBox = QtGui.QComboBox()
    comboBox.show()

    tableView = QtGui.QTableView()
    tableView.show()



    red   = QtGui.QColor(255,0,0)
    green = QtGui.QColor(0,255,0)
    blue  = QtGui.QColor(0,0,255)



    rowCount = 4
    columnCount = 6



    model = PaletteListModel([red, green, blue])
    model.insertRows(0, 5) #at zero index, insert five items (list!)

    listView.setModel(model)
    comboBox.setModel(model)
    tableView.setModel(model)
    treeView.setModel(model)


    sys.exit(app.exec_())
