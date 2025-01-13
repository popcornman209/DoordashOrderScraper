import sys
from lib.misc import log
from PySide6.QtCore import Qt, Slot, Signal
import PySide6.QtWidgets as qw


class mainWindow(qw.QWidget):
    def __init__(self):
        qw.QWidget.__init__(self)
        self.setWindowTitle("Doordash bot - Leo :)")
        self.resize(300,300)

        self.getButton = qw.QPushButton("get orders")
        self.viewButton = qw.QPushButton("view basic data")
        self.exportButton = qw.QPushButton("export data")
        self.settingsButton = qw.QPushButton("settings")
        self.updateButton = qw.QPushButton("update")

        self.message = qw.QLabel("if this ever breaks or is missing a feature, feel free to tell me!")
        self.message.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

        self.layout = qw.QVBoxLayout(self)
        self.layout.addWidget(self.getButton)
        self.layout.addWidget(self.viewButton)
        self.layout.addWidget(self.exportButton)
        self.layout.addWidget(self.settingsButton)
        self.layout.addWidget(self.updateButton)
        self.layout.addWidget(self.message)

        # Connecting the signal
        self.getButton.clicked.connect(self.openGetOrders)

        log("gui open")
    
    @Slot()
    def openGetOrders(self):
        self.setEnabled(False)
        self.ordersWindow = getOrdersWindow()
        self.ordersWindow.show()

class getOrdersWindow(qw.QWidget):
    closed = Signal()
    def __init__(self):
        qw.QWidget.__init__(self)
        self.setWindowTitle("get orders")
        self.resize(300,300)

        self.message = qw.QLabel("test :)")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout = qw.QVBoxLayout(self)
        self.layout.addWidget(self.message)

        # Connecting the signal
        #self.button.clicked.connect(sys.exit)

        log("gui open")
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

def run():
    log("starting gui...")
    app = qw.QApplication(sys.argv)

    window = mainWindow()
    window.show()

    sys.exit(app.exec_())