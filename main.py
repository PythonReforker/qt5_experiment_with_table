from selenium.webdriver import Chrome as Browser
import time
from queue import Queue
import re
import update_gui
from gui import Ui_MainWindow, QMainWindow
from PySide2.QtWidgets import QApplication, QFileDialog, QErrorMessage
import sys
import os
from os import path
import json
from qt_table_models import MessagesModel, Message, MessageFilterSortProxy

CONFIG_FILE = 'config.json'
LOGIN_URL = "https://www.paypal.com/signin"
PROFILE_URL = "https://www.paypal.com/myaccount/summary"
LOGIN_PASSWORD_FORMAT = re.compile(r"(?P<login>.+):(?P<password>.+)")
queue_auth_params = Queue(1)


def thread(queue: Queue):
    while True:
        lp = queue.get()
        br = Browser()
        matches = LOGIN_PASSWORD_FORMAT.match(lp)
        login, password = matches.group('login'), matches.group('password')
        br.get(LOGIN_URL)
        while not (tag := br.find_element_by_id("email")).is_displayed():
            time.sleep(0.1)
        tag.send_keys(login)
        completed = False
        while not completed:  # Может быть случай когда сначало логин и потом кнопку продолжить для пароля
            if (tag := br.find_element_by_id("password")).is_displayed():
                tag.send_keys(password)
                try:
                    br.find_element_by_id("btnLogin").click()
                    completed = True
                except:
                    ...
            elif (tag := br.find_element_by_id("btnNext")).is_displayed():
                try:
                    tag.click()
                except:
                    ...
            time.sleep(0.1)
        br.get(PROFILE_URL)
        while not (tag := br.find_element_by_class_name("cw_tile-currency")):
            time.sleep(0.1)
        print(tag.text)

class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.default_options = dict(
            login_file="",
            proxie_file="",
            path_to_tmp_files=path.join(os.getcwd(), 'tmp')
        )
        self.options = dict(**self.default_options)
        if path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                self.options.update(json.load(f))
        self.setupUi(self)
        self.table = MessagesModel()
        self.sorter_filter_table = MessageFilterSortProxy(self)
        self.sorter_filter_table.setSourceModel(self.table)
        self.sorter_filter_table.setDynamicSortFilter(True)
        self.table.insertRow(Message(login="11", proxie="22", text="33", status=0))
        self.tableView.setModel(self.sorter_filter_table)
        self.lineEdit.setText(self.options['path_to_tmp_files'])
        self.lineEdit_2.setText(self.options['login_file'])
        self.lineEdit_3.setText(self.options['proxie_file'])
        self.action.triggered.connect(self.open_file_login)
        self.action_2.triggered.connect(self.open_file_proxie)
        self.action_3.triggered.connect(self.clearOptions)
        self.action_4.triggered.connect(self.get_path_to_tmp_files)
        self.pushButton.clicked.connect(self.start_parser)
        self.pushButton_2.clicked.connect(self.stop_parser)
        self.qerrormessage = QErrorMessage(self)
        for i in range(10):
            self.table.insertRow(Message(login="11", proxie="22", text="33", status=i))
        self.show()

    def saveOptions(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.options, f)

    def clearOptions(self):
        self.options.update(self.default_options)
        self.lineEdit.setText(self.options['path_to_tmp_files'])
        self.lineEdit_2.setText(self.options['login_file'])
        self.lineEdit_3.setText(self.options['proxie_file'])
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.options, f)

    def open_file_login(self):
        file = QFileDialog.getOpenFileName(filter="""Текстовые файлы (*.txt)""")
        self.options['login_file'] = file[0]
        self.lineEdit_2.setText(file[0])
        self.saveOptions()

    def open_file_proxie(self):
        file = QFileDialog.getOpenFileName(filter="""Текстовые файлы (*.txt)""")
        self.options['proxie_file'] = file[0]
        self.lineEdit_3.setText(file[0])
        self.saveOptions()

    def start_parser(self):
        self.sorter_filter_table.setFilterRole()
        if self.options['login_file'] == "":
            self.qerrormessage.showMessage("Вы не задали файл логинов!")
        elif self.options['proxie_file'] == "":
            self.qerrormessage.showMessage("Вы не задали файл прокси!")
        else:
            self.pushButton.setDisabled(True)
            self.pushButton_2.setDisabled(False)

    def stop_parser(self):
        self.pushButton.setDisabled(False)
        self.pushButton_2.setDisabled(True)

    def get_path_to_tmp_files(self):
        path_to_tmp_files = QFileDialog.getExistingDirectory(self)
        self.options["path_to_tmp_files"] = path_to_tmp_files
        self.lineEdit.setText(path_to_tmp_files)
        self.saveOptions()

def main():
    app = QApplication(sys.argv)
    parser = App()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
