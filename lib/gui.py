import sys
from lib.misc import log
from PySide6.QtCore import Qt, Slot
import PySide6.QtWidgets as qw

class ordersPage:
    def __init__(self):
        self.page = qw.QWidget()
        self.layout = qw.QVBoxLayout(self.page)

        # Message
        self.message = qw.QLabel("get orders page")
        self.message.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.message)

        # Back and Get buttons at the bottom
        self.buttonLayout = qw.QHBoxLayout()
        self.backButton = qw.QPushButton("Back")
        self.getButton = qw.QPushButton("Get")
        # Connect signals for getButton as needed, e.g., getButton.clicked.connect(some_function)

        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.getButton)
        self.layout.addLayout(self.buttonLayout)
    @Slot()
    def show(self): self.containerWidget.setCurrentWidget(self.page)
    def initButton(self,method,widget):
        self.backButton.clicked.connect(method)
        self.containerWidget = widget

class mainPage:
    def __init__(self):
        self.page = qw.QWidget()
        self.layout = qw.QVBoxLayout(self.page)

        # Buttons
        self.getButton = qw.QPushButton("get orders")
        self.viewButton = qw.QPushButton("view basic data")
        self.exportButton = qw.QPushButton("export data")
        self.settingsButton = qw.QPushButton("settings")
        self.updateButton = qw.QPushButton("update")

        # Message
        self.message = qw.QLabel("If this ever breaks or is missing a feature, feel free to tell me!")
        self.message.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

        # Add widgets to layout
        self.layout.addWidget(self.getButton)
        self.layout.addWidget(self.viewButton)
        self.layout.addWidget(self.exportButton)
        self.layout.addWidget(self.settingsButton)
        self.layout.addWidget(self.updateButton)
        self.layout.addWidget(self.message)
        
    @Slot()
    def show(self): self.containerWidget.setCurrentWidget(self.page)
    def initButton(self,method,widget):
        self.getButton.clicked.connect(method)
        self.containerWidget = widget

class MainWindow(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Doordash bot - Leo :)")
        self.resize(300, 300)

        # Main layout and stacked widget
        self.layout = qw.QVBoxLayout(self)
        self.stackedWidget = qw.QStackedWidget()
        self.layout.addWidget(self.stackedWidget)

        # Adding pages to stacked widget
        self.mainPage = mainPage()
        self.ordersPage = ordersPage()

        self.mainPage.initButton(self.ordersPage.show,self.stackedWidget)
        self.ordersPage.initButton(self.mainPage.show,self.stackedWidget)

        self.stackedWidget.addWidget(self.mainPage.page)
        self.stackedWidget.addWidget(self.ordersPage.page)

        log("GUI open")


def run():
    log("Starting GUI...")
    app = qw.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())