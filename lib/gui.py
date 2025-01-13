import sys
from lib.misc import log
from PySide6.QtCore import Qt, Slot
import PySide6.QtWidgets as qw

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
        self.mainPage = self.createMainPage()
        self.getOrdersPage = self.createGetOrdersPage()

        self.stackedWidget.addWidget(self.mainPage)
        self.stackedWidget.addWidget(self.getOrdersPage)

        log("GUI open")

    def createMainPage(self):
        page = qw.QWidget()
        layout = qw.QVBoxLayout(page)

        # Buttons
        self.getButton = qw.QPushButton("get orders")
        self.viewButton = qw.QPushButton("view basic data")
        self.exportButton = qw.QPushButton("export data")
        self.settingsButton = qw.QPushButton("settings")
        self.updateButton = qw.QPushButton("update")

        # Message
        message = qw.QLabel("If this ever breaks or is missing a feature, feel free to tell me!")
        message.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

        # Add widgets to layout
        layout.addWidget(self.getButton)
        layout.addWidget(self.viewButton)
        layout.addWidget(self.exportButton)
        layout.addWidget(self.settingsButton)
        layout.addWidget(self.updateButton)
        layout.addWidget(message)

        # Connect button signal
        self.getButton.clicked.connect(self.showGetOrdersPage)

        return page

    def createGetOrdersPage(self):
        page = qw.QWidget()
        layout = qw.QVBoxLayout(page)

        # Message
        message = qw.QLabel("get orders page")
        message.setAlignment(Qt.AlignCenter)
        layout.addWidget(message)

        # Back and Get buttons at the bottom
        buttonLayout = qw.QHBoxLayout()
        backButton = qw.QPushButton("Back")
        backButton.clicked.connect(self.showMainPage)
        getButton = qw.QPushButton("Get")
        # Connect signals for getButton as needed, e.g., getButton.clicked.connect(some_function)

        buttonLayout.addWidget(backButton)
        buttonLayout.addWidget(getButton)
        layout.addLayout(buttonLayout)

        return page

    @Slot()
    def showGetOrdersPage(self): self.stackedWidget.setCurrentWidget(self.getOrdersPage)
    @Slot()
    def showMainPage(self): self.stackedWidget.setCurrentWidget(self.mainPage)

def run():
    log("Starting GUI...")
    app = qw.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())