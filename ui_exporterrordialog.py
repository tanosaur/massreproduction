# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_error.ui'
#
# Created: Thu Oct 15 00:43:59 2015
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

class Ui_ExportErrorDialog(object):
    def setupUi(self, ExportErrorDialog):
        ExportErrorDialog.setObjectName(_fromUtf8("ExportErrorDialog"))
        ExportErrorDialog.resize(263, 117)
        self.verticalLayout = QtGui.QVBoxLayout(ExportErrorDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(ExportErrorDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(ExportErrorDialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ExportErrorDialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), ExportErrorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ExportErrorDialog)

    def retranslateUi(self, ExportErrorDialog):
        ExportErrorDialog.setWindowTitle(_translate("ExportErrorDialog", "Export Error", None))
        self.label.setText(_translate("ExportErrorDialog", "Please provide reason(s) for manual range(s) applied.", None))
        self.pushButton.setText(_translate("ExportErrorDialog", "OK", None))

