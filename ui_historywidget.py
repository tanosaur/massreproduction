# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historywidget.ui'
#
# Created: Wed Jul 15 02:10:51 2015
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

class Ui_historyWidget(object):
    def setupUi(self, historyWidget):
        historyWidget.setObjectName(_fromUtf8("historyWidget"))
        historyWidget.resize(400, 300)

        self.retranslateUi(historyWidget)
        QtCore.QMetaObject.connectSlotsByName(historyWidget)

    def retranslateUi(self, historyWidget):
        historyWidget.setWindowTitle(_translate("historyWidget", "Form", None))

