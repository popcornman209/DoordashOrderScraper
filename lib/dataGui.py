import json,os
from lib.misc import log, BasePage, export
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QListWidget, QFileDialog

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
            items = ["{}:  ${}".format(person,round(data["spendings"][person],2)) for person in data["spendings"]]
            self.list_widget.addItems(items)
            self.show()
        else:
            self.dispMessageMethod("no data saved!",self.on_back)

class exportPage(BasePage):
    def __init__(self, container_widget: QStackedWidget, on_back: callable, dispMessage: callable):
        super().__init__(container_widget)

        self.on_back = on_back
        self.dispMessageMethod = dispMessage

        self.layout = QVBoxLayout(self.page)

        self.jsonButton = QPushButton("export JSON")
        self.csvButton = QPushButton("export CSV")
        self.layout.addWidget(self.jsonButton)
        self.layout.addWidget(self.csvButton)

        self.jsonButton.clicked.connect(self.exportJson)
        self.csvButton.clicked.connect(self.exportCsv)

        self.layout.addStretch()
        self.back_button = QPushButton("back")
        self.back_button.clicked.connect(self.on_back)
        self.layout.addWidget(self.back_button)
    
    def export(self,type):
        with open("data/output.json", "r") as f:
            data = json.load(f)
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Optional: Use for consistent appearance across platforms
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Select Destination for Export",
            "",  # Initial directory or file name
            "JSON Files (*.json);;All Files (*)" if type == "json" else "CSV Files (*.csv);;All Files (*)",  # Filter for file types
            options=options
        )
        export(data,type,file_path)
        
    
    def exportJson(self): self.export("json")
    def exportCsv(self): self.export("csv")
    
    def display(self):
        if os.path.exists("data/output.json"):
            self.show()
        else:
            self.dispMessageMethod("no data saved!",self.on_back)