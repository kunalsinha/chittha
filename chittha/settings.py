# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.setFixedSize(351, 251)
        Settings.setSizeGripEnabled(False)
        self.buttonBox = QtWidgets.QDialogButtonBox(Settings)
        self.buttonBox.setGeometry(QtCore.QRect(70, 200, 261, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Settings)
        self.label.setGeometry(QtCore.QRect(30, 40, 121, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Settings)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 71, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Settings)
        self.label_3.setGeometry(QtCore.QRect(30, 100, 31, 17))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Settings)
        self.pushButton.setGeometry(QtCore.QRect(260, 40, 71, 21))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Settings)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 70, 71, 21))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Settings)
        self.pushButton_3.setGeometry(QtCore.QRect(260, 100, 71, 21))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.checkBox = QtWidgets.QCheckBox(Settings)
        self.checkBox.setGeometry(QtCore.QRect(30, 150, 171, 23))
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.label.setText(_translate("Settings", "BackgroundColor"))
        self.label_2.setText(_translate("Settings", "Text Color"))
        self.label_3.setText(_translate("Settings", "Font"))
        self.checkBox.setText(_translate("Settings", "Run Chittha at startup"))


