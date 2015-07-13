from PyQt4 import QtGui, QtCore, uic
import sys

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    #http://pyqt.sourceforge.net/Docs/PyQt4/qapplication.html#details
    """The QApplication class manages the GUI application's control flow and main settings.

    QApplication contains the main event loop, where all events from the window system and other sources are processed and dispatched. It also handles the application's initialization, finalization, and provides session management. In addition, QApplication handles most of the system-wide and application-wide settings.

    For any GUI application using Qt, there is precisely one QApplication object, no matter whether the application has 0, 1, 2 or more windows at any given time. For non-GUI Qt applications, use QCoreApplication instead, as it does not depend on the QtGui library.

    The QApplication object is accessible through the instance() function that returns a pointer equivalent to the global qApp pointer.

    QApplication's main areas of responsibility are:

    It initializes the application with the user's desktop settings such as palette(), font() and doubleClickInterval(). It keeps track of these properties in case the user changes the desktop globally, for example through some kind of control panel.
    It performs event handling, meaning that it receives events from the underlying window system and dispatches them to the relevant widgets. By using sendEvent() and postEvent() you can send your own events to widgets.
    It parses common command line arguments and sets its internal state accordingly. See the constructor documentation below for more details.
    It defines the application's look and feel, which is encapsulated in a QStyle object. This can be changed at runtime with setStyle().
    It specifies how the application is to allocate colors. See setColorSpec() for details.
    It provides localization of strings that are visible to the user via translate().
    It provides some magical objects like the desktop() and the clipboard().
    It knows about the application's windows. You can ask which widget is at a certain position using widgetAt(), get a list of topLevelWidgets() and closeAllWindows(), etc.
    It manages the application's mouse cursor handling, see setOverrideCursor()
    On the X window system, it provides functions to flush and sync the communication stream, see flushX() and syncX().
    It provides support for sophisticated session management. This makes it possible for applications to terminate gracefully when the user logs out, to cancel a shutdown process if termination isn't possible and even to preserve the entire application's state for a future session. See isSessionRestored(), sessionId() and commitData() and saveState() for details.
    Since the QApplication object does so much initialization, it must be created before any other objects related to the user interface are created. QApplication also deals with common command line arguments. Hence, it is usually a good idea to create it before any interpretation or modification of argv is done in the application itself."""

    app.setStyle("cleanlooks")
    #Specifically modify application style

    #DATA
    data = QtCore.QStringList() # Same as Python list but dedicated to QString
    data << "one" << "two" << "three" << "four" << "five"
    # Also provides this convenient operator, rather than having to do the .append(itemone), etc.


    listView = QtGui.QListView()
    listView.show()

    # BAD: ITEM-BASED SYSTEM
    # listwidget.additems(data)
    # count = listWidget.count()
    # for i in range(count):
        # item=listWidget.item(i)
        # item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    # comboBox=QtGui.QComboBox()
    # combobox.show()
    # comboBox.addItems(data)

    # When you rename it in the list widget, it does not update in the combo box!
    # The list widget (item-based) and the combo box have stored separate instances of the data.

    # GOOD: MODEL-VIEW SYSTEM

    model = QtGui.QStringListModel(data)


    listView.setModel(model)

    listView2 = QtGui.QListView()
    listView2.show() # Empty window
    listView2.setModel(model) # Now filled with model of data!

    combobox = QtGui.QComboBox()
    combobox.setModel(model)
    combobox.show()

    # Now all 3 widgets use the same model, and all are updated when any are changed.

    sys.exit(app.exec_())
