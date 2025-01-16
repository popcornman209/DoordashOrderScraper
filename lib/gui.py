import sys,json
import lib.orderPageGui as ordPage
import lib.dataGui as dataGui
import lib.update as updPage
from lib.misc import log, BasePage, basicMessage
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QWidget

with open("configs/loginInfo.json","r") as f:
    accountInfo = json.load(f) #load default account info

class MainPage(BasePage):
    def __init__(self, container_widget: QStackedWidget, on_orders: callable, viewBasic: callable, exportPage: callable, updateMethod: callable):
        super().__init__(container_widget)
        self.layout = QVBoxLayout(self.page)

        # Add buttons
        buttons = [ #buttons on main page and there methods to run
            ("Get Orders", on_orders),
            ("View Basic Data", viewBasic),
            ("Export Data", exportPage),
            ("Update", updateMethod),
        ]

        for text, callback in buttons: #go through each button
            button = QPushButton(text) #make the button
            if callback:
                button.clicked.connect(callback) #set there method
            self.layout.addWidget(button) #add to screen

        # Add message
        message = QLabel("If this ever breaks or is missing a feature, feel free to tell me!") # :)
        message.setAlignment(Qt.AlignBottom | Qt.AlignCenter) #throw at the bottom of the screen
        
        self.layout.addWidget(message)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Doordash Bot - Leo :)")
        self.resize(300, 400)

        # Main layout and stacked widget
        layout = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Initialize pages
        self.main_page = MainPage(self.stacked_widget, self.showOrdersPage, self.showBasicData, self.showExportPage, self.updateMethod) #main page
        self.basic_message_page = basicMessage(self.stacked_widget) #basic menu page, for displaying mesages

        self.selectOrdersPage = ordPage.orderSelector(self.stacked_widget) #select orders page, for doing just that
        self.orders_page = ordPage.OrdersPage(self.stacked_widget, self.showMainPage, self.basic_message_page.dispMessage, self.selectOrdersPage) #main orders page, runs the main script

        self.basicDataPage = dataGui.viewBasic(self.stacked_widget, self.showMainPage, self.basic_message_page.dispMessage) #displays total spendings and last ran date/time
        self.exportPage = dataGui.exportPage(self.stacked_widget,self.showMainPage,self.basic_message_page.dispMessage) #for exporting the data as a csv or json
        self.updatePage = updPage.updatePage(self.basic_message_page.dispMessage,self.showMainPage) #basic method for updating the app

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.main_page.page)
        self.stacked_widget.addWidget(self.selectOrdersPage.page)
        self.stacked_widget.addWidget(self.orders_page.page)
        self.stacked_widget.addWidget(self.basic_message_page.page)
        self.stacked_widget.addWidget(self.basicDataPage.page)
        self.stacked_widget.addWidget(self.exportPage.page)

        log("GUI open")

    #all of these are because situations like the main menu page needing the order page to be initialized first, and vice versa.
    #if i make a function below to run a method on a page, i can get around this issue easily.
    def showMainPage(self): self.main_page.show()
    def showOrdersPage(self): self.orders_page.show()
    def showBasicData(self): self.basicDataPage.display()
    def showExportPage(self): self.exportPage.display()
    def updateMethod(self): self.updatePage.update()


def run(): #runs main gui
    log("Starting GUI...")
    app = QApplication(sys.argv) #main application

    window = MainWindow() #main window
    window.show()

    sys.exit(app.exec()) #run the app
