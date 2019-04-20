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
        self.confirmationBox = QtWidgets.QDialogButtonBox(Settings)
        self.confirmationBox.setGeometry(QtCore.QRect(70, 200, 261, 32))
        self.confirmationBox.setOrientation(QtCore.Qt.Horizontal)
        self.confirmationBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirmationBox.setObjectName("confirmationBox")
        self.bgColorLabel = QtWidgets.QLabel(Settings)
        self.bgColorLabel.setGeometry(QtCore.QRect(30, 40, 121, 17))
        self.bgColorLabel.setObjectName("bgColorLabel")
        self.textColorLabel = QtWidgets.QLabel(Settings)
        self.textColorLabel.setGeometry(QtCore.QRect(30, 70, 71, 17))
        self.textColorLabel.setObjectName("textColorLabel")
        self.fontLabel = QtWidgets.QLabel(Settings)
        self.fontLabel.setGeometry(QtCore.QRect(30, 100, 31, 17))
        self.fontLabel.setObjectName("fontLabel")
        self.bgColorButton = QtWidgets.QPushButton(Settings)
        self.bgColorButton.setGeometry(QtCore.QRect(260, 40, 71, 21))
        self.bgColorButton.setText("")
        self.bgColorButton.setObjectName("bgColorButton")
        self.textColorButton = QtWidgets.QPushButton(Settings)
        self.textColorButton.setGeometry(QtCore.QRect(260, 70, 71, 21))
        self.textColorButton.setText("")
        self.textColorButton.setObjectName("textColorButton")
        self.fontButton = QtWidgets.QPushButton(Settings)
        self.fontButton.setGeometry(QtCore.QRect(260, 100, 71, 21))
        self.fontButton.setText("")
        self.fontButton.setObjectName("fontButton")
        self.startUpCheckBox = QtWidgets.QCheckBox(Settings)
        self.startUpCheckBox.setGeometry(QtCore.QRect(30, 150, 171, 23))
        self.startUpCheckBox.setObjectName("startUpCheckBox")

        self.retranslateUi(Settings)
        self.confirmationBox.accepted.connect(Settings.accept)
        self.confirmationBox.rejected.connect(Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.bgColorLabel.setText(_translate("Settings", "BackgroundColor"))
        self.textColorLabel.setText(_translate("Settings", "Text Color"))
        self.fontLabel.setText(_translate("Settings", "Font"))
        self.startUpCheckBox.setText(_translate("Settings", "Run Chittha at startup"))


