# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Mon Apr 27 17:54:05 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(441, 277)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 6, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.D000bButton = QtGui.QPushButton(Dialog)
        self.D000bButton.setObjectName(_fromUtf8("D000bButton"))
        self.gridLayout.addWidget(self.D000bButton, 5, 1, 1, 1)
        self.D000cButton = QtGui.QPushButton(Dialog)
        self.D000cButton.setObjectName(_fromUtf8("D000cButton"))
        self.gridLayout.addWidget(self.D000cButton, 6, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 2)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 2, 0, 1, 2)
        self.D000aButton = QtGui.QPushButton(Dialog)
        self.D000aButton.setObjectName(_fromUtf8("D000aButton"))
        self.gridLayout.addWidget(self.D000aButton, 4, 1, 1, 1)
        self.saveButton = QtGui.QPushButton(Dialog)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.gridLayout.addWidget(self.saveButton, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.outputLabel = QtGui.QLabel(Dialog)
        self.outputLabel.setObjectName(_fromUtf8("outputLabel"))
        self.verticalLayout_2.addWidget(self.outputLabel)
        self.textBrowser = QtGui.QTextBrowser(Dialog)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.label_2.setBuddy(self.D000aButton)
        self.label.setBuddy(self.D000cButton)
        self.label_3.setBuddy(self.D000bButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_2.setText(_translate("Dialog", "000&a", None))
        self.label.setText(_translate("Dialog", "000&c", None))
        self.label_3.setText(_translate("Dialog", "000&b", None))
        self.D000bButton.setText(_translate("Dialog", "DO", None))
        self.D000cButton.setText(_translate("Dialog", "DO", None))
        self.label_4.setText(_translate("Dialog", "Enter text:", None))
        self.D000aButton.setText(_translate("Dialog", "DO", None))
        self.saveButton.setText(_translate("Dialog", "Save", None))
        self.outputLabel.setText(_translate("Dialog", "TextLabel", None))

