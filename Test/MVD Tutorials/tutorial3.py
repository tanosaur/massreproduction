from PyQt4 import QtGui, QtCore, uic
import sys




# Must subclass any abstract model

class PaletteTableModel(QtCore.QAbstractListModel):

    def __init__(self, colors=[[]], headers=[], parent=None):
        QtCore.QAbstractListModel.__init__(self,parent) #The super class constructor, passing parent argument.
        self.__colors=colors # Store input color list in a private list
        self.__headers=headers

    #EVERY MODEL MUST IMPLEMENT 2 METHODS AT MIN IN PYQT
    # 'data' and 'rowcount'
    # Or you'll get empty windows even if model-view set up and working.

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                return self.__headers[section]
            else:
                return QtCore.QString("Color %1").arg(section)


    def rowCount(self, parent): # Can ignore the parent parameter if working on list, not tree.
        """Tell view how many items model contains.
        View needs to know so it can ask for the data within the
        rowcount range."""
        return len(self.__colors) #default row count

    def columnCount(self,parent):
        return len(self.__colors[0]) #no of cols in each row (assume same cols in each row)

    def data(self, index, role):
        """View will call data for every row which the row count method returns"""

        row=index.row()
        column=index.column()

        if role == QtCore.Qt.EditRole:
            return self.__colors[row][column].name()


        if role == QtCore.Qt.ToolTipRole:
            return "Hex code: " + self.__colors[row][column].name()


        if role == QtCore.Qt.DecorationRole:


            value = self.__colors[row][column]

            pixmap = QtGui.QPixmap(26, 26)
            pixmap.fill(value)

            icon = QtGui.QIcon(pixmap)

            return icon


        if role == QtCore.Qt.DisplayRole:

            value = self.__colors[row][column]

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
            column=index.column()
            color = QtGui.QColor(value) #value hopefully contains hex code for color

            if color.isValid(): #if so
                self.__colors[row][column]= color
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






if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)


    #ALL OF OUR VIEWS
    listView = QtGui.QListView()
    listView.show()

    # treeView = QtGui.QTreeView()
    # treeView.show()

    comboBox = QtGui.QComboBox()
    comboBox.show()

    tableView = QtGui.QTableView()
    tableView.show()



    red   = QtGui.QColor(255,0,0)
    green = QtGui.QColor(0,255,0)
    blue  = QtGui.QColor(0,0,255)

    # tableData0=[['0', '1', '2', '3'], ['4', '5', '6', '7'], ['8','9','10','11'], ['12','13','14','15']]

    # Need QColor objects instead of string inputs.

    rowCount = 4
    columnCount = 6
    headers=['Palette', 'Colors', 'Omg', 'Technical', 'Artist']
    tableData0=[ [QtGui.QColor('#FFFF00') for i in range(columnCount)] for j in range(rowCount) ]
    model=PaletteTableModel(tableData0, headers)

    # model = PaletteListModel([red, green, blue])
    # model.insertRows(0, 5) #at zero index, insert five items (list!)

    listView.setModel(model)
    comboBox.setModel(model)
    tableView.setModel(model) #CAN'T BE USED WITH 3 VIEWS IT CRASHES WHEN EXPANDING ??
    # treeView.setModel(model)


    sys.exit(app.exec_())
