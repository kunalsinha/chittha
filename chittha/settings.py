# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from chittha.note import NoteManager


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.setFixedSize(551, 251)
        Settings.setSizeGripEnabled(False)
        # confirmation buttons
        self.confirmationBox = QtWidgets.QDialogButtonBox(Settings)
        self.confirmationBox.setGeometry(QtCore.QRect(270, 200, 261, 32))
        self.confirmationBox.setOrientation(QtCore.Qt.Horizontal)
        self.confirmationBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.confirmationBox.setObjectName("confirmationBox")
        # labels
        self.bgColorLabel = QtWidgets.QLabel(Settings)
        self.bgColorLabel.setGeometry(QtCore.QRect(30, 40, 121, 17))
        self.bgColorLabel.setObjectName("bgColorLabel")
        self.textColorLabel = QtWidgets.QLabel(Settings)
        self.textColorLabel.setGeometry(QtCore.QRect(30, 70, 71, 17))
        self.textColorLabel.setObjectName("textColorLabel")
        self.fontLabel = QtWidgets.QLabel(Settings)
        self.fontLabel.setGeometry(QtCore.QRect(30, 100, 31, 17))
        self.fontLabel.setObjectName("fontLabel")
        # background color settings
        self.bgColorButton = QtWidgets.QPushButton(Settings)
        self.bgColorButton.setGeometry(QtCore.QRect(430, 40, 101, 21))
        self.bgColorButton.setText("")
        self.bgColorButton.setObjectName("bgColorButton")
        self.bgColorButton.clicked.connect(self.pickBgColor)
        self.bgColorButton.setStyleSheet('background-color: yellow;')
        # text color settings
        self.textColorButton = QtWidgets.QPushButton(Settings)
        self.textColorButton.setGeometry(QtCore.QRect(430, 70, 101, 21))
        self.textColorButton.setText("")
        self.textColorButton.setObjectName("textColorButton")
        self.textColorButton.clicked.connect(self.pickTextColor)
        self.textColorButton.setStyleSheet('background-color: black;')
        # font settings
        self.fontButton = QtWidgets.QPushButton(Settings)
        self.fontButton.setGeometry(QtCore.QRect(250, 100, 281, 21))
        self.fontButton.setText("Ubuntu")
        self.fontButton.setObjectName("fontButton")
        self.fontPicker = QtWidgets.QFontDialog(Settings)
        self.fontButton.clicked.connect(self.pickFont)
        # startup settings
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

    def pickBgColor(self):
        color = QtWidgets.QColorDialog.getColor()
        self.bgColorButton.setStyleSheet('background-color: ' + color.name() + ';')
        NoteManager.updateBgColor(color)

    def pickTextColor(self):
        color = QtWidgets.QColorDialog.getColor()
        self.textColorButton.setStyleSheet('background-color: ' + color.name() + ';')
        NoteManager.updateTextColor(color)

    def pickFont(self):
        font, ok = self.fontPicker.getFont()
        if ok:
            name = None
            weight = ''
            style = ''
            fontFamily = font.family()
            fontWeight = font.weight()
            fontStyle = font.style()
            if fontWeight == QFont.Thin:
                weight = 'Thin'
            elif fontWeight == QFont.ExtraLight:
                weight = 'ExtraLight'
            elif fontWeight == QFont.Light:
                weight = 'Light'
            elif fontWeight == QFont.Normal:
                weight = ''
            elif fontWeight == QFont.Medium:
                weight = 'Medium'
            elif fontWeight == QFont.DemiBold:
                weight = 'DemiBold'
            elif fontWeight == QFont.Bold:
                weight = 'Bold'
            elif fontWeight == QFont.ExtraBold:
                weight = 'ExtraBold'
            elif fontWeight == QFont.Black:
                weight = 'Black'
            if fontStyle == QFont.StyleNormal:
                style = ''
            elif fontStyle == QFont.StyleItalic:
                style = 'Italic'
            elif fontStyle == QFont.StyleOblique:
                style = 'Oblique'
            name = fontFamily + ' ' + weight + ' ' + style
            self.fontButton.setText(name + ' | ' + str(font.pointSize()))
            NoteManager.updateFont(font)

    def save(self):
        pass

    def load(self):
        pass

