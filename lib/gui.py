import sys,json
import lib.orderPageGui as ordPage
from lib.misc import log, BasePage, basicMessage
from PySide6.QtCore import QThread, Qt, Slot, Signal
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QWidget, QCheckBox, QSpinBox, QLineEdit

with open("configs/loginInfo.json","r") as f:
    accountInfo = json.load(f)

class MainPage(BasePage):
    def __init__(self, container_widget: QStackedWidget, on_orders: callable):
        super().__init__(container_widget)
        self.layout = QVBoxLayout(self.page)

        # Add buttons
        buttons = [
            ("Get Orders", on_orders),
            ("View Basic Data", None),
            ("Export Data", None),
            ("Settings", None),
            ("Update", None),
        ]

        for text, callback in buttons:
            button = QPushButton(text)
            if callback:
                button.clicked.connect(callback)
            self.layout.addWidget(button)

        # Add message
        message = QLabel("If this ever breaks or is missing a feature, feel free to tell me!")
        message.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        
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
        self.main_page = MainPage(self.stacked_widget, self.showOrdersPage)
        self.basic_message_page = basicMessage(self.stacked_widget)

        self.orders_page = ordPage.OrdersPage(self.stacked_widget, self.showMainPage,self.basic_message_page.dispMessage)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.main_page.page)
        self.stacked_widget.addWidget(self.orders_page.page)
        self.stacked_widget.addWidget(self.basic_message_page.page)

        log("GUI open")

    def showMainPage(self): self.main_page.show()
    def showOrdersPage(self): self.orders_page.show()


def run():
    log("Starting GUI...")
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
