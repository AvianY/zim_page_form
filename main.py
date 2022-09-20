# This Python file uses the following encoding: utf-8
import os, re, sys
from typing import Optional
from venv import create
from xmlrpc.client import ResponseError
from PySide2.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

from dokuwiki import DokuWikiError

from zim_tools import is_zim_file, zim_pagepath_regex, zim_pagepath_to_filepath, create_pdf_from_json, zim_filepath_to_json, get_media_from_json, json_to_dokuwiki, filepath_to_zim_pagepath
from buildform_helpers import get_config, get_config_filepath, get_credentials, get_notebook_folder, catch_value_error, get_project_name
from zim_pages_selector import ZimPagesSelector
from upload_dokuwiki import upload_files_to_dokuwiki, delete_files_from_dokuwiki
from pathlib import Path
from configparser import ConfigParser
from argparse import ArgumentParser
import itertools
import json



def flatten(l):
    return [item for sublist in l for item in sublist]

class BuildForm(QWidget):
    def __init__(self, notebook_folder, filepaths, config: ConfigParser, project_name):
        super(BuildForm, self).__init__()
        self.ui = self.load_ui()

        self.select_notebook_folder(notebook_folder)
        
        for i, project in enumerate(config.keys()):
            self.ui.project_comboBox.addItem(project)
            if project_name is not None and project == project_name:
                self.ui.project_comboBox.setCurrentIndex(i)
                self.project_changed(i)
        if self.ui.project_comboBox.currentIndex() == -1 and project_name is not None:
            QMessageBox.warning(self, 'Missing project', f'Could not find the project_name "{project_name}"')
        
        if project_name is None:
            self.ui.project_comboBox.setCurrentIndex(-1)
        
        self.ui.project_comboBox.currentIndexChanged.connect(self.project_changed)
        self.ui.notebook_folder_browse_button.clicked.connect(self.select_notebook_folder)
        self.ui.pagepath_browse_button.clicked.connect(self.open_zim_pages_selector)
        self.ui.generate_Button.clicked.connect(self.save_fonfiguration)
        self.ui.delete_from_server_pushButton.clicked.connect(self.delete_selected_files)
        self.ui.generate_pdf_Button.clicked.connect(self.generate_pdf)
        self.ui.upload_to_server_Button.clicked.connect(self.upload_selected_files)

        if self.ui.pagepath_listWidget.count() == 0:
            self.select_pages(filepaths)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui


    @catch_value_error
    def project_changed(self, index):
        if index == -1:
            return
        notebook_folder_config = get_config(self)
        project_name = self.ui.project_comboBox.currentText()

        project_section = notebook_folder_config[project_name]

        filepaths = []
        for i in itertools.count():
            if f'page_{i}' in project_section:
                filepaths.append(project_section[f'page_{i}'])
            else:
                break
        
        self.select_pages(filepaths)
        
        self.ui.server_lineEdit.setText(project_section.get('server', ''))
        self.ui.username_lineEdit.setText(project_section.get('username', ''))
        self.ui.password_lineEdit.setText(project_section.get('password', ''))

        self.ui.title_lineEdit.setText(project_section.get('title', ''))
        self.ui.author_lineEdit.setText(project_section.get('author', ''))
        self.ui.date_lineEdit.setText(project_section.get('date', ''))
        self.ui.keywords_lineEdit.setText(project_section.get('keywords', ''))
        self.ui.languages_lineEdit.setText(project_section.get('languages', ''))
        self.ui.margin_lineEdit.setText(project_section.get('margin', ''))
        self.ui.table_of_contents_checkBox.setChecked(True if project_section.get('table_of_contents') == 'yes' else False)

    @catch_value_error
    def upload_selected_files(self) -> None:
        notebook_folder = get_notebook_folder(self)

        lwlen = self.ui.pagepath_listWidget.count()
        filepaths = [Path(self.ui.pagepath_listWidget.item(i).text()) for i in range(lwlen)]

        json_files = [zim_filepath_to_json(notebook_folder / filepath) for filepath in filepaths]

        media_filepaths = list(set(flatten(get_media_from_json(content) for content in json_files)))
        media_pagepaths = [filepath_to_zim_pagepath(filepath, keepSuffix=True) for filepath in media_filepaths]
        media_files = []
        for filepath in media_filepaths:
            with open(notebook_folder / filepath, 'rb') as f:
                media_files.append(f.read())

        dokuwiki_pagepaths = [filepath_to_zim_pagepath(filepath) for filepath in filepaths]
        dokuwiki_files = [json_to_dokuwiki(content) for content in json_files]

        pages = dict((pagepath, file) for pagepath, file in zip(dokuwiki_pagepaths, dokuwiki_files))
        media = dict((pagepath, file) for pagepath, file in zip(media_pagepaths, media_files))

        credentials = get_credentials(self)
        try:
            upload_files_to_dokuwiki(pages, media, credentials)
        except DokuWikiError as err:
            QMessageBox.warning(self, 'Upload error', f'unable to connect: {err}')
            return
        except ResponseError as err:
            QMessageBox.warning(self, 'Upload error', f'Response error: {err}')
            return
        QMessageBox.information(self, 'Success', 'Files successfully uploaded to dokuwiki')


    @catch_value_error
    def delete_selected_files(self):
        notebook_folder = get_notebook_folder(self)

        lwlen = self.ui.pagepath_listWidget.count()
        filepaths = [Path(self.ui.pagepath_listWidget.item(i).text()) for i in range(lwlen)]

        json_files = [zim_filepath_to_json(notebook_folder / filepath) for filepath in filepaths]

        media_filepaths = list(set(flatten(get_media_from_json(content) for content in json_files)))
        media_pagepaths = [filepath_to_zim_pagepath(filepath, keepSuffix=True) for filepath in media_filepaths]
        dokuwiki_pagepaths = [filepath_to_zim_pagepath(filepath) for filepath in filepaths]

        credentials = get_credentials(self)
        try:
            delete_files_from_dokuwiki(dokuwiki_pagepaths, media_pagepaths, credentials)
        except DokuWikiError as err:
            QMessageBox.warning(self, 'Deletion error', f'unable to connect: {err}')
            return
        except ResponseError as err:
            QMessageBox.warning(self, 'Deletion error', f'Response error: {err}')
            return
        QMessageBox.information(self, 'Success', 'Files successfully deleted from dokuwiki')


        
    @catch_value_error
    def generate_pdf(self):
        notebook_folder = get_notebook_folder(self)
        lwlen = self.ui.pagepath_listWidget.count()

        filepaths = [Path(self.ui.pagepath_listWidget.item(i).text()) for i in range(lwlen)]

        json_files = [zim_filepath_to_json(filepath) for filepath in filepaths]

        json_dicts = [json.loads(json_file) for json_file in json_files]
        merged_json_dict = {'pandoc-api-version': json_dicts[0]['pandoc-api-version'], 'meta': {}, 'blocks': []}
        for i in range(0, len(json_dicts)):
            merged_json_dict['blocks'].append({"t":"RawBlock","c":["tex","\\newpage"]})
            for block in json_dicts[i]['blocks']:
                merged_json_dict['blocks'].append(block)
        pdf_options = [
            '--metadata', 'title:' + self.ui.title_lineEdit.text(),
            '--metadata', 'author:' + self.ui.author_lineEdit.text(),
            '--metadata', 'date:' + self.ui.date_lineEdit.text(),
            '--metadata', 'keywords:' + self.ui.keywords_lineEdit.text(),
            '--metadata', 'lang:' + self.ui.languages_lineEdit.text(),
            '--metadata', 'margin:' + self.ui.margin_lineEdit.text(),
            '--metadata', 'block-headings:true',
            '--metadata', 'document-class:report'
        ]

        if self.ui.table_of_contents_checkBox.isChecked():
            pdf_options.append('--table-of-contents')

        try:
            pdf_content = create_pdf_from_json(json.dumps(merged_json_dict), pdf_options)
        except:
            QMessageBox.information(self, 'Failure', 'Could not generate the pdf.')
            return


        with open(notebook_folder / 'documentation.pdf', 'wb') as f:
            f.write(pdf_content)
        QMessageBox.information(self, 'Success', 'The pdf was successfully created.')

    @catch_value_error
    def open_zim_pages_selector(self):
        notebook_folder = get_notebook_folder(self)
        self.selector_window = ZimPagesSelector(self, notebook_folder)        
        self.selector_window.show()

    def select_notebook_folder(self, folderpath: Optional[Path]=None):
        if not folderpath:
            folderpath = QFileDialog.getExistingDirectory(self, 'Select Notebook folder')
        if folderpath in [None, '']:
            return
        if not (Path(folderpath) / 'notebook.zim').is_file():
            QMessageBox.warning(self, 'Not a zim notebook', 'Selected folder is not a zim notebook.')
            return

        self.ui.notebook_folder_lineEdit.setText(str(folderpath))

    @catch_value_error
    def select_pages(self, filepaths=None):
        notebook_folder = get_notebook_folder(self)
    
        for filepath in filepaths:
            if not is_zim_file(notebook_folder / filepath):
                QMessageBox.warning(self, 'Not a zim file', f'The file "{notebook_folder / filepath}" is not a zim file.')
                return

        self.ui.pagepath_listWidget.clear()
        self.ui.pagepath_listWidget.addItems([str(filepath) for filepath in filepaths])

    @catch_value_error
    def save_fonfiguration(self):
        config_filepath = get_config_filepath(self)
        project_name = get_project_name(self)

        lwlen = self.ui.pagepath_listWidget.count()
        filepaths = [self.ui.pagepath_listWidget.item(i).text() for i in range(lwlen)]

        notebook_folder_config = get_config(self)

        if project_name not in notebook_folder_config:
            notebook_folder_config.add_section(project_name)
        
        project_section = notebook_folder_config[project_name]

        for i in itertools.count():
            if f'page_{i}' in project_section:
                project_section.pop(f'page_{i}')
            else:
                break
        for i, pagepath in enumerate(filepaths):
            project_section[f'page_{i}'] = pagepath

        project_section['server'] = self.ui.server_lineEdit.text()
        project_section['username'] = self.ui.username_lineEdit.text()
        project_section['password'] = self.ui.password_lineEdit.text()

        project_section['title'] = self.ui.title_lineEdit.text()
        project_section['author'] = self.ui.author_lineEdit.text()
        project_section['date'] = self.ui.date_lineEdit.text()
        project_section['keywords'] = self.ui.keywords_lineEdit.text()
        project_section['languages'] = self.ui.languages_lineEdit.text()
        project_section['margin'] = self.ui.margin_lineEdit.text()
        project_section['table_of_contents'] = 'true' if self.ui.table_of_contents_checkBox.isChecked() else 'false'
        
        with open(config_filepath, 'w') as f:
            notebook_folder_config.write(f)

        QMessageBox.warning(self, 'Success', 'Your configuration was successfully saved')



if __name__ == "__main__":
    parser = ArgumentParser(description='A form for easier conversion and uploading of zim pages')
    parser.add_argument('pagepaths', nargs='*', help='Either pagepaths or filepaths of the zim pages')
    parser.add_argument('--notebook-folder', help='The path to the target notebook folder')
    parser.add_argument('--project-name', help='The name of the project')

    parsed = parser.parse_args()

    app = QApplication(sys.argv)

    if parsed.notebook_folder is None:
        notebook_folder = Path(QFileDialog.getExistingDirectory(None, 'Select Notebook folder'))
    else:
        notebook_folder = Path(parsed.notebook_folder)

    try:
        notebook_config = ConfigParser()
        notebook_config.read(notebook_folder / 'notebook.zim')
        config_filepath = notebook_folder / (notebook_config['Notebook']['name'] + '.conf')
    except:
        QMessageBox.warning(None, 'Not a zim notebook', 'Selected folder is not a zim notebook.')
        sys.exit(-1)


    config: dict = {}
    if os.path.isfile(config_filepath):
        parser = ConfigParser()
        parser.read(config_filepath)
        config = {s:dict(parser.items(s)) for s in parser.sections()}
        
    filepaths = []
    for pagepath in parsed.pagepaths:
        if re.match(zim_pagepath_regex, pagepath) and not os.path.isfile(notebook_folder / pagepath):
            filepaths.append(zim_pagepath_to_filepath(pagepath))
        else:
            filepaths.append(Path(pagepath))


    window = BuildForm(notebook_folder, filepaths, config, parsed.project_name)
    window.show()

    sys.exit(app.exec_())
