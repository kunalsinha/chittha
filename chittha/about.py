# Chittha - a sticky notes application
# Copyright (C) 2019 Kunal Sinha <kunalsinha4u@gmail.com>
#
# Chittha is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Chittha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Chittha.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(540, 351)
        self.about = QtWidgets.QWidget()
        self.about.setEnabled(True)
        self.about.setObjectName("about")
        self.label_2 = QtWidgets.QLabel(self.about)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 511, 321))
        self.label_2.setObjectName("label_2")
        TabWidget.addTab(self.about, "")
        self.license = QtWidgets.QWidget()
        self.license.setObjectName("license")
        self.label = QtWidgets.QLabel(self.license)
        self.label.setGeometry(QtCore.QRect(20, 10, 481, 241))
        self.label.setObjectName("label")
        TabWidget.addTab(self.license, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "Chittha"))
        self.label_2.setText(_translate("TabWidget", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Chittha v1.0</span></p><p align=\"center\"><span style=\" font-weight:600;\">Keyboard Shortcuts</span></p><p align=\"center\">Ctrl + N -&gt; New note</p><p align=\"center\">Ctrl + L -&gt; Lock/Unlock note</p><p align=\"center\">Ctrl + J -&gt; Next note</p><p align=\"center\">Ctrl + K -&gt; Previous note</p><p align=\"center\">Ctrl + H -&gt; Hide all notes</p><p align=\"center\">Ctrl + P -&gt; Always on top</p><p align=\"center\"><br/></p><p align=\"center\"><a href=\"https://github.com/kunalsinha/chittha\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/kunalsinha/chittha</span></a></p><p align=\"center\">Copyright (C) 2019 Kunal Sinha</p></body></html>"))
        TabWidget.setTabText(TabWidget.indexOf(self.about), _translate("TabWidget", "About"))
        self.label.setText(_translate("TabWidget", "Chittha is free software: you can redistribute it and/or modify\n"
"it under the terms of the GNU General Public License as published by\n"
"the Free Software Foundation, either version 3 of the License, or\n"
"(at your option) any later version.\n"
"\n"
"Chittha is distributed in the hope that it will be useful,\n"
"but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
"MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
"GNU General Public License for more details.\n"
"\n"
"You should have received a copy of the GNU General Public License\n"
"along with Chittha.  If not, see <https://www.gnu.org/licenses/>."))
        TabWidget.setTabText(TabWidget.indexOf(self.license), _translate("TabWidget", "License"))

