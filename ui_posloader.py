# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'posloader.ui'
#
# Created: Tue Jul 14 06:23:48 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_loadDialog(object):
    def setupUi(self, loadDialog):
        loadDialog.setObjectName(_fromUtf8("loadDialog"))
        loadDialog.resize(581, 365)
        # loadDialog.setToolTipDuration(-6)
        self.verticalLayout_2 = QtGui.QVBoxLayout(loadDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.selectLabel = QtGui.QLabel(loadDialog)
        self.selectLabel.setObjectName(_fromUtf8("selectLabel"))
        self.horizontalLayout_2.addWidget(self.selectLabel)
        self.posButton = QtGui.QPushButton(loadDialog)
        self.posButton.setObjectName(_fromUtf8("posButton"))
        self.horizontalLayout_2.addWidget(self.posButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.posLabel = QtGui.QLabel(loadDialog)
        self.posLabel.setObjectName(_fromUtf8("posLabel"))
        self.horizontalLayout.addWidget(self.posLabel)
        self.removeButton = QtGui.QPushButton(loadDialog)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.horizontalLayout.addWidget(self.removeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.knownelementsLabel = QtGui.QLabel(loadDialog)
        self.knownelementsLabel.setObjectName(_fromUtf8("knownelementsLabel"))
        self.verticalLayout.addWidget(self.knownelementsLabel)
        self.knownelementsLineEdit = QtGui.QLineEdit(loadDialog)
        self.knownelementsLineEdit.setObjectName(_fromUtf8("knownelementsLineEdit"))
        self.verticalLayout.addWidget(self.knownelementsLineEdit)
        self.maxchargestateLabel = QtGui.QLabel(loadDialog)
        self.maxchargestateLabel.setObjectName(_fromUtf8("maxchargestateLabel"))
        self.verticalLayout.addWidget(self.maxchargestateLabel)
        self.maxchargestateLineEdit = QtGui.QLineEdit(loadDialog)
        self.maxchargestateLineEdit.setObjectName(_fromUtf8("maxchargestateLineEdit"))
        self.verticalLayout.addWidget(self.maxchargestateLineEdit)
        self.rangemethodLabel = QtGui.QLabel(loadDialog)
        self.rangemethodLabel.setObjectName(_fromUtf8("rangemethodLabel"))
        self.verticalLayout.addWidget(self.rangemethodLabel)
        self.rangemethodComboBox = QtGui.QComboBox(loadDialog)
        self.rangemethodComboBox.setObjectName(_fromUtf8("rangemethodComboBox"))
        self.rangemethodComboBox.addItem(_fromUtf8(""))
        self.rangemethodComboBox.addItem(_fromUtf8(""))
        self.rangemethodComboBox.addItem(_fromUtf8(""))
        self.rangemethodComboBox.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.rangemethodComboBox)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(loadDialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_3.addWidget(self.cancelButton)
        self.loadButton = QtGui.QPushButton(loadDialog)
        self.loadButton.setEnabled(False)
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.horizontalLayout_3.addWidget(self.loadButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.actionUndo = QtGui.QAction(loadDialog)
        self.actionUndo.setObjectName(_fromUtf8("actionUndo"))
        self.actionRedo = QtGui.QAction(loadDialog)
        self.actionRedo.setObjectName(_fromUtf8("actionRedo"))
        self.posLabel.setBuddy(self.posButton)

        self.retranslateUi(loadDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), loadDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(loadDialog)

    def retranslateUi(self, loadDialog):
        loadDialog.setWindowTitle(_translate("loadDialog", "Dialog", None))
        self.selectLabel.setText(_translate("loadDialog", "Select .pos or .epos file(s)", None))
        self.posButton.setText(_translate("loadDialog", "Add", None))
        self.posLabel.setText(_translate("loadDialog", "-", None))
        self.removeButton.setText(_translate("loadDialog", "Remove", None))
        self.knownelementsLabel.setText(_translate("loadDialog", "Known Elements (comma-separated)", None))
        self.maxchargestateLabel.setText(_translate("loadDialog", "Max. charge state (absolute value)", None))
        self.rangemethodLabel.setText(_translate("loadDialog", "Range method", None))
        self.rangemethodComboBox.setItemText(0, _translate("loadDialog", "Select...", None))
        self.rangemethodComboBox.setItemText(1, _translate("loadDialog", "FWHM", None))
        self.rangemethodComboBox.setItemText(2, _translate("loadDialog", "FWTM", None))
        self.rangemethodComboBox.setItemText(3, _translate("loadDialog", "Manual", None))
        self.cancelButton.setText(_translate("loadDialog", "Cancel", None))
        self.loadButton.setText(_translate("loadDialog", "Load", None))
        self.actionUndo.setText(_translate("loadDialog", "Undo", None))
        self.actionUndo.setShortcut(_translate("loadDialog", "Ctrl+Z", None))
        self.actionRedo.setText(_translate("loadDialog", "Redo", None))
        self.actionRedo.setShortcut(_translate("loadDialog", "Ctrl+Shift+Z", None))
