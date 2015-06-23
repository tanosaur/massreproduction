# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'posloader.ui'
#
# Created: Fri May  8 14:28:49 2015
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
        loadDialog.resize(470, 352)
        self.verticalLayout_2 = QtGui.QVBoxLayout(loadDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.posButton = QtGui.QPushButton(loadDialog)
        self.posButton.setObjectName(_fromUtf8("posButton"))
        self.horizontalLayout.addWidget(self.posButton)
        self.posLabel = QtGui.QLabel(loadDialog)
        self.posLabel.setObjectName(_fromUtf8("posLabel"))
        self.horizontalLayout.addWidget(self.posLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.addButton = QtGui.QPushButton(loadDialog)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout_3.addWidget(self.addButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(loadDialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_3.addWidget(self.cancelButton)
        self.loadButton = QtGui.QPushButton(loadDialog)
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.horizontalLayout_3.addWidget(self.loadButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.posLabel.setBuddy(self.posButton)

        self.retranslateUi(loadDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), loadDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(loadDialog)

    def retranslateUi(self, loadDialog):
        loadDialog.setWindowTitle(_translate("loadDialog", "Dialog", None))
        self.posButton.setText(_translate("loadDialog", "Select .&pos file", None))
        self.posLabel.setText(_translate("loadDialog", "-", None))
        self.addButton.setText(_translate("loadDialog", "Add", None))
        self.cancelButton.setText(_translate("loadDialog", "Cancel", None))
        self.loadButton.setText(_translate("loadDialog", "Load", None))

