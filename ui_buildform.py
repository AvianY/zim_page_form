# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_BuildForm(object):
    def setupUi(self, BuildForm):
        if not BuildForm.objectName():
            BuildForm.setObjectName(u"BuildForm")
        BuildForm.resize(756, 656)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BuildForm.sizePolicy().hasHeightForWidth())
        BuildForm.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(BuildForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(20, -1, 20, -1)
        self.line = QFrame(BuildForm)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 24, 0, 1, 3)

        self.label_4 = QLabel(BuildForm)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 17, 0, 1, 1)

        self.label_15 = QLabel(BuildForm)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 23, 0, 1, 1)

        self.label_6 = QLabel(BuildForm)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 19, 0, 1, 1)

        self.username_lineEdit = QLineEdit(BuildForm)
        self.username_lineEdit.setObjectName(u"username_lineEdit")

        self.gridLayout.addWidget(self.username_lineEdit, 13, 2, 1, 1)

        self.password_lineEdit = QLineEdit(BuildForm)
        self.password_lineEdit.setObjectName(u"password_lineEdit")
        self.password_lineEdit.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.password_lineEdit, 14, 2, 1, 1)

        self.date_lineEdit = QLineEdit(BuildForm)
        self.date_lineEdit.setObjectName(u"date_lineEdit")

        self.gridLayout.addWidget(self.date_lineEdit, 19, 2, 1, 1)

        self.table_of_contents_checkBox = QCheckBox(BuildForm)
        self.table_of_contents_checkBox.setObjectName(u"table_of_contents_checkBox")

        self.gridLayout.addWidget(self.table_of_contents_checkBox, 23, 2, 1, 1)

        self.label_10 = QLabel(BuildForm)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 10, 2, 1, 1)

        self.label = QLabel(BuildForm)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 12, 0, 1, 1)

        self.label_14 = QLabel(BuildForm)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 22, 0, 1, 1)

        self.line_2 = QFrame(BuildForm)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 15, 0, 1, 3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pagepath_listWidget = QListWidget(BuildForm)
        self.pagepath_listWidget.setObjectName(u"pagepath_listWidget")
        self.pagepath_listWidget.setSelectionMode(QAbstractItemView.NoSelection)

        self.horizontalLayout_2.addWidget(self.pagepath_listWidget)

        self.pagepath_browse_button = QPushButton(BuildForm)
        self.pagepath_browse_button.setObjectName(u"pagepath_browse_button")

        self.horizontalLayout_2.addWidget(self.pagepath_browse_button)


        self.gridLayout.addLayout(self.horizontalLayout_2, 7, 2, 1, 1)

        self.label_3 = QLabel(BuildForm)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 14, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 26, 0, 1, 1)

        self.label_16 = QLabel(BuildForm)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 2, 0, 1, 1)

        self.margin_lineEdit = QLineEdit(BuildForm)
        self.margin_lineEdit.setObjectName(u"margin_lineEdit")

        self.gridLayout.addWidget(self.margin_lineEdit, 22, 2, 1, 1)

        self.line_4 = QFrame(BuildForm)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_4, 9, 0, 1, 3)

        self.project_comboBox = QComboBox(BuildForm)
        self.project_comboBox.setObjectName(u"project_comboBox")
        self.project_comboBox.setEditable(True)

        self.gridLayout.addWidget(self.project_comboBox, 2, 2, 1, 1)

        self.label_11 = QLabel(BuildForm)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 16, 2, 1, 1)

        self.title_lineEdit = QLineEdit(BuildForm)
        self.title_lineEdit.setObjectName(u"title_lineEdit")

        self.gridLayout.addWidget(self.title_lineEdit, 17, 2, 1, 1)

        self.languages_lineEdit = QLineEdit(BuildForm)
        self.languages_lineEdit.setObjectName(u"languages_lineEdit")

        self.gridLayout.addWidget(self.languages_lineEdit, 21, 2, 1, 1)

        self.label_12 = QLabel(BuildForm)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 20, 0, 1, 1)

        self.label_13 = QLabel(BuildForm)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 21, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.notebook_folder_lineEdit = QLineEdit(BuildForm)
        self.notebook_folder_lineEdit.setObjectName(u"notebook_folder_lineEdit")
        self.notebook_folder_lineEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.notebook_folder_lineEdit)

        self.notebook_folder_browse_button = QPushButton(BuildForm)
        self.notebook_folder_browse_button.setObjectName(u"notebook_folder_browse_button")

        self.horizontalLayout.addWidget(self.notebook_folder_browse_button)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 2, 1, 1)

        self.keywords_lineEdit = QLineEdit(BuildForm)
        self.keywords_lineEdit.setObjectName(u"keywords_lineEdit")

        self.gridLayout.addWidget(self.keywords_lineEdit, 20, 2, 1, 1)

        self.label_2 = QLabel(BuildForm)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 13, 0, 1, 1)

        self.label_5 = QLabel(BuildForm)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 18, 0, 1, 1)

        self.server_lineEdit = QLineEdit(BuildForm)
        self.server_lineEdit.setObjectName(u"server_lineEdit")

        self.gridLayout.addWidget(self.server_lineEdit, 12, 2, 1, 1)

        self.label_9 = QLabel(BuildForm)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 2, 1, 1)

        self.author_lineEdit = QLineEdit(BuildForm)
        self.author_lineEdit.setObjectName(u"author_lineEdit")

        self.gridLayout.addWidget(self.author_lineEdit, 18, 2, 1, 1)

        self.label_8 = QLabel(BuildForm)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)

        self.label_7 = QLabel(BuildForm)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.generate_pdf_Button = QPushButton(BuildForm)
        self.generate_pdf_Button.setObjectName(u"generate_pdf_Button")

        self.horizontalLayout_5.addWidget(self.generate_pdf_Button)

        self.upload_to_server_Button = QPushButton(BuildForm)
        self.upload_to_server_Button.setObjectName(u"upload_to_server_Button")

        self.horizontalLayout_5.addWidget(self.upload_to_server_Button)

        self.delete_from_server_pushButton = QPushButton(BuildForm)
        self.delete_from_server_pushButton.setObjectName(u"delete_from_server_pushButton")

        self.horizontalLayout_5.addWidget(self.delete_from_server_pushButton)


        self.gridLayout.addLayout(self.horizontalLayout_5, 28, 0, 1, 3)

        self.generate_Button = QPushButton(BuildForm)
        self.generate_Button.setObjectName(u"generate_Button")

        self.gridLayout.addWidget(self.generate_Button, 27, 0, 1, 1)

        QWidget.setTabOrder(self.notebook_folder_browse_button, self.pagepath_browse_button)
        QWidget.setTabOrder(self.pagepath_browse_button, self.server_lineEdit)
        QWidget.setTabOrder(self.server_lineEdit, self.username_lineEdit)
        QWidget.setTabOrder(self.username_lineEdit, self.password_lineEdit)
        QWidget.setTabOrder(self.password_lineEdit, self.title_lineEdit)
        QWidget.setTabOrder(self.title_lineEdit, self.author_lineEdit)
        QWidget.setTabOrder(self.author_lineEdit, self.date_lineEdit)
        QWidget.setTabOrder(self.date_lineEdit, self.keywords_lineEdit)
        QWidget.setTabOrder(self.keywords_lineEdit, self.languages_lineEdit)
        QWidget.setTabOrder(self.languages_lineEdit, self.margin_lineEdit)
        QWidget.setTabOrder(self.margin_lineEdit, self.table_of_contents_checkBox)
        QWidget.setTabOrder(self.table_of_contents_checkBox, self.generate_pdf_Button)
        QWidget.setTabOrder(self.generate_pdf_Button, self.upload_to_server_Button)
        QWidget.setTabOrder(self.upload_to_server_Button, self.notebook_folder_lineEdit)

        self.retranslateUi(BuildForm)

        QMetaObject.connectSlotsByName(BuildForm)
    # setupUi

    def retranslateUi(self, BuildForm):
        BuildForm.setWindowTitle(QCoreApplication.translate("BuildForm", u"BuildForm", None))
        self.label_4.setText(QCoreApplication.translate("BuildForm", u"Title", None))
        self.label_15.setText(QCoreApplication.translate("BuildForm", u"Table of contents", None))
        self.label_6.setText(QCoreApplication.translate("BuildForm", u"Date", None))
        self.table_of_contents_checkBox.setText("")
        self.label_10.setText(QCoreApplication.translate("BuildForm", u"Server credentials", None))
        self.label.setText(QCoreApplication.translate("BuildForm", u"Dokuwiki server", None))
        self.label_14.setText(QCoreApplication.translate("BuildForm", u"Margin", None))
        self.pagepath_browse_button.setText(QCoreApplication.translate("BuildForm", u"Select", None))
        self.label_3.setText(QCoreApplication.translate("BuildForm", u"Dokuwiki password", None))
        self.label_16.setText(QCoreApplication.translate("BuildForm", u"Project", None))
        self.margin_lineEdit.setText(QCoreApplication.translate("BuildForm", u"1in", None))
        self.label_11.setText(QCoreApplication.translate("BuildForm", u"PDF document settings", None))
        self.label_12.setText(QCoreApplication.translate("BuildForm", u"Keywords", None))
        self.label_13.setText(QCoreApplication.translate("BuildForm", u"Languages", None))
        self.notebook_folder_browse_button.setText(QCoreApplication.translate("BuildForm", u"Browse", None))
        self.label_2.setText(QCoreApplication.translate("BuildForm", u"Dokuwiki username", None))
        self.label_5.setText(QCoreApplication.translate("BuildForm", u"Author", None))
        self.label_9.setText(QCoreApplication.translate("BuildForm", u"Notebook settings", None))
        self.label_8.setText(QCoreApplication.translate("BuildForm", u"Notebook folder", None))
        self.label_7.setText(QCoreApplication.translate("BuildForm", u"Pagepaths", None))
        self.generate_pdf_Button.setText(QCoreApplication.translate("BuildForm", u"Generate pdf document", None))
        self.upload_to_server_Button.setText(QCoreApplication.translate("BuildForm", u"upload to server", None))
        self.delete_from_server_pushButton.setText(QCoreApplication.translate("BuildForm", u"delete from server", None))
        self.generate_Button.setText(QCoreApplication.translate("BuildForm", u"Save configuration", None))
    # retranslateUi

