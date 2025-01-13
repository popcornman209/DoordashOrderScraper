import sys
from lib.misc import log
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget)


class mainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.button = QPushButton("Click me!")
        self.message = QLabel("Hello World")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.button)

        # Connecting the signal
        self.button.clicked.connect(sys.exit)


def run():
    log("starting gui...")
    app = QApplication(sys.argv)

    window = mainWindow()
    window.show()

    sys.exit(app.exec_())