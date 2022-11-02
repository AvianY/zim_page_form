from genericpath import isfile
import re
from PySide2.QtWidgets import QMessageBox
from configparser import ConfigParser
from pathlib import Path
import os
from zim_tools import zim_pagepath_regex

def get_notebook_folder(buildForm):
    notebook_folder = buildForm.ui.notebook_folder_lineEdit.text().strip()
    if notebook_folder == '':
        QMessageBox.warning(buildForm, 'Notebook folder missing', 'Notebook folder is necessary for this operation')
        raise ValueError("notebook_folder")
    return Path(notebook_folder)

def get_selected_pages(buildForm):
    selected_indexes = buildForm.selector_window.ui.listView.selectionModel().selectedIndexes()
    if len(selected_indexes) == 0:
        QMessageBox.warning(buildForm, 'No pages selected', 'Zim pages are necessary for this operation')
        raise ValueError("selected_pages")

    return [index.data() for index in selected_indexes]

def get_zim_pages(buildForm):
    pass

def get_credentials(buildForm):
    if buildForm.ui.server_lineEdit.text() == '':
        QMessageBox.warning(buildForm, 'Server URL missing', 'Server URL is necessary for this operation')
        raise ValueError('credentials_server')
    if buildForm.ui.username_lineEdit.text() == '':
        QMessageBox.warning(buildForm, 'Dokuwiki username missing', 'Dokuwiki username is necessary for this operation')
        raise ValueError('credentials_username')
    if buildForm.ui.password_lineEdit.text() == '':
        QMessageBox.warning(buildForm, 'Dokuwiki password missing', 'Dokuwiki password is necessary for this operation')
        raise ValueError('credentials_password')
    return {
        'server': buildForm.ui.server_lineEdit.text(),
        'username': buildForm.ui.username_lineEdit.text(),
        'password': buildForm.ui.password_lineEdit.text()
    }


def get_notebook_name(buildForm):
    notebook_folder = get_notebook_folder(buildForm)
    config = ConfigParser()
    config.read(notebook_folder / 'notebook.zim')
    return config['Notebook']['name']

def get_config_filepath(buildForm, requireExists=False):
    notebook_name = get_notebook_name(buildForm)
    notebook_folder = get_notebook_folder(buildForm)
    config_filepath = notebook_folder / (notebook_name + '.conf')
    if requireExists and not os.path.isfile(config_filepath):
        QMessageBox.warning(buildForm, 'Config missing', 'The config is necessary for this operation')
        raise ValueError('Config')
    return config_filepath

def get_config(buildForm):
    config_filepath = get_config_filepath(buildForm)
    notebook_folder_config = ConfigParser(strict=False)
    notebook_folder_config.read(config_filepath)
    return notebook_folder_config

def get_project_name(buildForm):
    project_name = buildForm.ui.project_comboBox.currentText().strip()
    if project_name == '':
        QMessageBox.warning(buildForm, 'Project name missing', 'The project name is necessary for this operation')
        raise ValueError('Project')
    return project_name

def get_makefile_path(buildForm, requireExists=False):
    notebook_folder = get_notebook_folder(buildForm)
    makefile_name = Path(f'{get_notebook_name(buildForm)}_makefile')
    if requireExists and not (notebook_folder / makefile_name).is_file():
        QMessageBox.warning(buildForm, 'Makefile missing', 'A Makefile is necessary for this operation')
        raise ValueError('Makefile')

    return f'{get_notebook_name(buildForm)}_makefile'


def catch_value_error(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as err:
            QMessageBox.warning(None, f"{func.__name__} failed", str(err))
    return inner_function


def quote(obj):
    if isinstance(obj, list):
        return ['"' + string + '"' for string in obj]
    return '"' + obj + '"'

def get_prefix(buildForm):
    prefix = buildForm.ui.prefix_lineEdit.text()
    if prefix != '' and re.match(zim_pagepath_regex, prefix) is None:
        QMessageBox.warning(buildForm, 'Input error', f'the provided "prefix" field is invalid')
        return
    if prefix != '' and prefix[-1] != ':':
        prefix = prefix + ':'
    return prefix