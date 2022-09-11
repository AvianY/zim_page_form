# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'zim_pages_selector.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(375, 423)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.listView = QListView(Form)
        self.listView.setObjectName(u"listView")
        self.listView.setMinimumSize(QSize(200, 200))
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.setDragEnabled(False)
        self.listView.setDragDropOverwriteMode(False)
        self.listView.setDragDropMode(QAbstractItemView.InternalMove)
        self.listView.setDefaultDropAction(Qt.MoveAction)
        self.listView.setSelectionMode(QAbstractItemView.MultiSelection)

        self.gridLayout_2.addWidget(self.listView, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.remove_unselected_Button = QPushButton(Form)
        self.remove_unselected_Button.setObjectName(u"remove_unselected_Button")

        self.horizontalLayout.addWidget(self.remove_unselected_Button)

        self.confirm_Button = QPushButton(Form)
        self.confirm_Button.setObjectName(u"confirm_Button")

        self.horizontalLayout.addWidget(self.confirm_Button)


        self.gridLayout_2.addLayout(self.horizontalLayout, 6, 0, 1, 1)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.multiple_select_radioButton = QRadioButton(self.groupBox)
        self.multiple_select_radioButton.setObjectName(u"multiple_select_radioButton")
        self.multiple_select_radioButton.setChecked(True)

        self.horizontalLayout_2.addWidget(self.multiple_select_radioButton)

        self.single_select_radioButton = QRadioButton(self.groupBox)
        self.single_select_radioButton.setObjectName(u"single_select_radioButton")

        self.horizontalLayout_2.addWidget(self.single_select_radioButton)


        self.gridLayout_2.addWidget(self.groupBox, 4, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.remove_unselected_Button.setText(QCoreApplication.translate("Form", u"Remove unselected", None))
        self.confirm_Button.setText(QCoreApplication.translate("Form", u"confirm", None))
        self.groupBox.setTitle("")
        self.multiple_select_radioButton.setText(QCoreApplication.translate("Form", u"multipleselect", None))
        self.single_select_radioButton.setText(QCoreApplication.translate("Form", u"singleselect", None))
    # retranslateUi

