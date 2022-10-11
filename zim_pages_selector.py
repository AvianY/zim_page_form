import os
from PySide2.QtWidgets import QWidget, QMessageBox
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import Qt

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

from pathlib import Path

from zim_tools import find_zim_pagepaths, filepath_to_zim_pagepath
from printers.get_page_dependencies import get_page_dependencies


class ZimPagesSelector(QWidget):
    def __init__(self, parent, notebook_folder):
        super(ZimPagesSelector, self).__init__()
        self.ui = self.load_ui()

        self.parent = parent
        self.notebook_folder = notebook_folder

        self.ui.multiple_select_radioButton.clicked.connect(self.set_multiple_select)
        self.ui.single_select_radioButton.clicked.connect(self.set_single_select)
        self.ui.remove_unselected_Button.clicked.connect(self.remove_unselected)
        self.ui.confirm_Button.clicked.connect(self.confirm_selected)

        self.model = QStandardItemModel()
        filepaths = [str(filepath.relative_to(notebook_folder)) for filepath in find_zim_pagepaths(notebook_folder)]
        for i in range(len(filepaths)):
            item = QStandardItem(filepaths[i])
            item.setFlags(item.flags() ^ Qt.ItemIsDropEnabled)
            item.setFlags(item.flags() ^ Qt.ItemIsDragEnabled)
            self.model.appendRow(item)
        self.ui.listView.setModel(self.model)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "ui_files/zim_pages_selector.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui

    def set_multiple_select(self):
        self.ui.listView.setSelectionMode(self.ui.listView.MultiSelection)
        for i in range(self.model.rowCount()):
            item = self.model.item(i, 0)
            item.setFlags(item.flags() ^ Qt.ItemIsDragEnabled)
        

    def set_single_select(self):
        self.ui.listView.setSelectionMode(self.ui.listView.SingleSelection)
        self.ui.listView.clearSelection()
        for i in range(self.model.rowCount()):
            item = self.model.item(i, 0)
            item.setFlags(item.flags() | Qt.ItemIsDragEnabled)

    def remove_unselected(self):
        if self.ui.listView.selectionMode() != self.ui.listView.MultiSelection:
            return
        j = 0
        for i in range(self.model.rowCount()):
            selected_indexes = self.ui.listView.selectionModel().selectedIndexes()
            if len(selected_indexes) == 0: return
            if self.model.index(i - j, 0) not in selected_indexes:
                self.model.removeRow(i - j)
                j += 1

    def confirm_selected(self):
        selected_indexes = self.ui.listView.selectionModel().selectedIndexes()
        if len(selected_indexes) == 0:
            QMessageBox.warning(self, 'Cannot confirm', 'No page is selected.')
            self.selector_window.activateWindow()
            return
        
        selection_mode = self.ui.listView.selectionMode()
        self.parent.ui.pagepath_listWidget.clear()
        if selection_mode == self.ui.listView.SingleSelection:
            selected_filepath = Path(selected_indexes[-1].data())
            page_dependencies = get_page_dependencies([filepath_to_zim_pagepath(selected_filepath)], self.notebook_folder, self.notebook_folder)
            self.parent.ui.pagepath_listWidget.addItems([str(dependency.relative_to(self.notebook_folder)) for dependency in page_dependencies])
        else:
            self.parent.ui.pagepath_listWidget.addItems(index.data() for index in selected_indexes)
        
        self.close()
