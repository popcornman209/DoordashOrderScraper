import json,os
from lib.misc import log, BasePage, export
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QListWidget, QFileDialog

class viewBasic(BasePage):
    def __init__(self, container_widget: QStackedWidget, on_back: callable, dispMessage: callable):
        super().__init__(container_widget)

        self.on_back = on_back
        self.dispMessageMethod = dispMessage

        self.layout = QVBoxLayout(self.page)

        self.topText = QLabel("placeholder text") #place holder text for last ran date
        self.list_widget = QListWidget() #list of people and spendings
        self.layout.addWidget(self.topText)
        self.layout.addWidget(self.list_widget)

        self.layout.addStretch()
        self.back_button = QPushButton("back") #back button
        self.back_button.clicked.connect(self.on_back)
        self.layout.addWidget(self.back_button)

    def display(self):
        if os.path.exists("data/output.json"): #if there is data
            with open("data/output.json") as f:
                data = json.load(f) #load the data
            self.topText.setText("last ran: {}".format(data["lastRan"])) #set text to last ran
            self.list_widget.clear() #clear previous data
            items = ["{}:  ${}".format(person,round(data["spendings"][person],2)) for person in data["spendings"]] #make list of items
            self.list_widget.addItems(items) #display em
            self.show() #show the page
        else:
            self.dispMessageMethod("no data saved!",self.on_back)

class exportPage(BasePage):
    def __init__(self, container_widget: QStackedWidget, on_back: callable, dispMessage: callable):
        super().__init__(container_widget)

        self.on_back = on_back #main menu method
        self.dispMessageMethod = dispMessage #display message method

        self.layout = QVBoxLayout(self.page)

        self.jsonButton = QPushButton("export JSON") #two buttons
        self.csvButton = QPushButton("export CSV")
        self.layout.addWidget(self.jsonButton)
        self.layout.addWidget(self.csvButton)

        self.jsonButton.clicked.connect(self.exportJson)
        self.csvButton.clicked.connect(self.exportCsv)

        self.layout.addStretch()
        self.back_button = QPushButton("back") #back button
        self.back_button.clicked.connect(self.on_back)
        self.layout.addWidget(self.back_button)
    
    def export(self,type): #main export function
        with open("data/output.json", "r") as f:
            data = json.load(f) #load data

        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        
        options = QFileDialog.Options() #open file browser for save location
        options |= QFileDialog.DontUseNativeDialog  # Optional: Use for consistent appearance across platforms
        default_name = "output.json" if type == "json" else "output.csv" #default name for file

        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Select Destination for Export",
            os.path.join(downloads_folder, default_name),  # Initial directory or file name
            "JSON Files (*.json);;All Files (*)" if type == "json" else "CSV Files (*.csv);;All Files (*)",  # Filter for file types
            options=options
        )
        if file_path: export(data,type,file_path) #export :)
        
    
    def exportJson(self): self.export("json") #functions for either button
    def exportCsv(self): self.export("csv")
    
    def display(self): #display window
        if os.path.exists("data/output.json"):
            self.show() #if data exists, display page
        else: #otherwise tell user there isnt any data
            self.dispMessageMethod("no data saved!",self.on_back)