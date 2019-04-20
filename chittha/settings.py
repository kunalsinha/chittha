from PyQt5.QtWidgets import *

class Settings(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(Profile())
        self.layout.addWidget(Profile())
        self.layout.addWidget(Profile())

class Profile(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        # profile name
        self.name = QLabel('profile', self)
        self.layout.addWidget(self.name, 0, 0, 1, 1)
        self.nameField = QLineEdit(self)
        self.layout.addWidget(self.nameField, 0, 1, 1, 1)
        # background color
        self.bgColor = QLabel('Background Color', self)
        self.layout.addWidget(self.bgColor, 1, 0, 1, 1)
        self.bgColorPicker = QPushButton(self)
        self.bgColorDialog = QColorDialog(self)
        self.bgColorPicker.clicked.connect(self.bgColorDialog.show)
        self.layout.addWidget(self.bgColorPicker, 1, 1, 1, 1)
        # text color
        self.textColor = QLabel('Text Color', self)
        self.layout.addWidget(self.textColor, 2, 0, 1, 1)
        self.textColorPicker = QPushButton(self)
        self.textColorDialog = QColorDialog(self)
        self.textColorPicker.clicked.connect(self.textColorDialog.show)
        self.layout.addWidget(self.textColorPicker, 2, 1, 1, 1)
        # font
        self.font = QLabel('Font', self)
        self.layout.addWidget(self.font, 3, 0, 1, 1)
        self.fontPicker = QPushButton(self)
        self.fontDialog = QFontDialog(self)
        self.fontPicker.clicked.connect(self.fontDialog.show)
        self.layout.addWidget(self.fontPicker, 3, 1, 1, 1)
