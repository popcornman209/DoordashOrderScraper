import sys,json,os
from lib.misc import log, BasePage
from PySide6.QtCore import QThread, Qt, Slot, Signal
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QWidget, QCheckBox, QSpinBox, QLineEdit, QListWidget

class viewBasic(BasePage):
    def __init__(self, container_widget: QStackedWidget, on_back: callable, dispMessage: callable):
        super().__init__(container_widget)

        self.on_back = on_back
        self.dispMessageMethod = dispMessage

        self.layout = QVBoxLayout(self.page)

        self.topText = QLabel("placeholder text")
        self.list_widget = QListWidget()
        self.layout.addWidget(self.topText)
        self.layout.addWidget(self.list_widget)

        self.layout.addStretch()
        self.back_button = QPushButton("back")
        self.back_button.clicked.connect(self.on_back)
        self.layout.addWidget(self.back_button)

    def display(self):
        if os.path.exists("data/output.json"):
            with open("data/output.json") as f:
                data = json.load(f)
            self.topText.setText("last ran: {}".format(data["lastRan"]))
            self.list_widget.clear()
            items = ["{}:  ${}".format(person,data["spendings"][person]) for person in data["spendings"]]
            self.list_widget.addItems(items)
            self.show()

class export(BasePage):
    def __init__(self, container_widget: QStackedWidget, on_back: callable, dispMessage: callable):
        super().__init__(container_widget)

        self.on_back = on_back
        self.dispMessageMethod = dispMessage

        self.layout = QVBoxLayout(self.page)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.layout.addStretch()
        self.back_button = QPushButton("back")
        self.back_button.clicked.connect(self.on_back)
        self.layout.addWidget(self.back_button)

    def display(self):
        if os.path.exists("data/output.json"):
            with open("data/output.json") as f:
                data = json.load(f)
            self.list_widget.clear()
            items = ["{}:  ${}".format(person,data["spendings"][person]) for person in data["spendings"]]
            self.list_widget.addItems(items)
            self.show()