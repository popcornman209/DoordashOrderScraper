import sys,json
from lib.misc import log, BasePage
from PySide6.QtCore import QThread, Qt, Slot, Signal
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QWidget, QCheckBox, QSpinBox, QLineEdit

with open("configs/loginInfo.json","r") as f:
    accountInfo = json.load(f)

class mainScriptWorker(QThread):
    update_message_signal = Signal(tuple)  # Signal to update the message
    finished_signal = Signal()

    def __init__(self, orderWindow):
        super().__init__()
        self.orderWindow = orderWindow

    def run(self):
        import lib.mainScript as mScript
        bHeadless = self.orderWindow.widgets["headLessBrowser"].isChecked()
        days = self.orderWindow.widgets["daysField"].value() if self.orderWindow.widgets["autoSelectOrders"].isChecked() else -1
        accInfo = {
            "autoLogin": self.orderWindow.widgets["autoLogin"].isChecked(),
            "DDusername": self.orderWindow.widgets["emailField"].text(),
            "DDpassword": self.orderWindow.widgets["passField"].text()
        }

        mScript.main(False, bHeadless, days, accountInfo=accInfo, displayMessageMethod=self.on_message_update, savePath="data/output.json",mainPageMethod=self.orderWindow.on_back)
        self.finished_signal.emit()
    
    def on_message_update(self, message, method=None):
        self.update_message_signal.emit((message,method))

class basicMessage(BasePage):
    def __init__(self, container_widget: QStackedWidget):
        super().__init__(container_widget)

        self.buttonMethod = None
        self.layout = QVBoxLayout(self.page)

        self.message = QLabel("<text here lol>")
        self.message.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.message)

        self.layout.addStretch()
        self.bottomMessage = QLabel("working...")
        self.bottomMessage.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.bottomMessage)

        self.continueButton = QPushButton("continue")
        self.layout.addWidget(self.continueButton)
    def dispMessage(self,text,method = None):
        self.message.setText(text)
        if self.buttonMethod:
            self.continueButton.clicked.disconnect(self.buttonMethod)
            self.buttonMethod = None
        if method:
            self.continueButton.setVisible(True)
            self.bottomMessage.setVisible(False)
            self.continueButton.clicked.connect(method)
            self.buttonMethod = method
            log("showed basic button menu")
        else:
            self.continueButton.setVisible(False)
            self.bottomMessage.setVisible(True)
            log("showed basic menu")
        self.show()

class OrdersPage(BasePage):
    def __init__(self, container_widget: QStackedWidget, on_back: callable, dispMessage: callable):
        super().__init__(container_widget)

        self.on_back = on_back
        self.dispMessageMethod = dispMessage
        self.mainWorker = mainScriptWorker(self)
        self.mainWorker.update_message_signal.connect(self.dispMessage)

        main_layout = QVBoxLayout(self.page)

        self.widgets = {
            "headLessBrowser": QCheckBox("headless (hide browser window)"), #headless browser checkbox
            "autoSelectOrders": QCheckBox("automatically select orders"), #wether to manuall select orders
            "daysText": QLabel("days to get in past:"), #text for following text field
            "daysField": QSpinBox(), #days in past text field
            "autoLogin": QCheckBox("auto login (required if headless)"), #auto login check box
            "emailText": QLabel("email/username:"), #email: text
            "emailField": QLineEdit(accountInfo["DDusername"]), #email field
            "passText": QLabel("password:"), #password: text
            "passField": QLineEdit(accountInfo["DDpassword"]) #password field
        }
        
        for widget in self.widgets:
            main_layout.addWidget(self.widgets[widget], alignment=Qt.AlignHCenter) #puts all of the widgets in the layout
        
        self.widgets["autoSelectOrders"].stateChanged.connect(self.manualCheckBoxChanged) #toggle days in past objects when swithed
        self.manualCheckBoxChanged(False) #hide said objects

        self.widgets["daysField"].setValue(7) #sets default value for days in past
        self.widgets["daysField"].setRange(0, 364) #sets minimum

        if accountInfo["autoLogin"]: self.widgets["autoLogin"].setCheckState(Qt.Checked) #if autologin setting on, set on by default
        else: self.loginCheckBoxChanged(False) #otherwise hide other objects
        self.widgets["autoLogin"].stateChanged.connect(self.loginCheckBoxChanged) #toggles login objects when autologin switched
        self.widgets["emailField"].setFixedWidth(250) #fixed width for email field
        self.widgets["passField"].setEchoMode(QLineEdit.Password) #hide password
        self.widgets["passField"].setFixedWidth(250) #fixed width for password field

        main_layout.addStretch()

        # Add back and get buttons
        button_layout = QHBoxLayout()
        back_button = QPushButton("back")
        get_button = QPushButton("continue")
        back_button.clicked.connect(self.on_back)
        get_button.clicked.connect(self.get)

        button_layout.addWidget(back_button)
        button_layout.addWidget(get_button)
        main_layout.addLayout(button_layout)
    
    def dispMessage(self,data):
        self.dispMessageMethod(data[0],method=data[1])
    def manualCheckBoxChanged(self,state):
        self.widgets["daysText"].setVisible(state)
        self.widgets["daysField"].setVisible(state)
    def loginCheckBoxChanged(self,state):
        self.widgets["emailText"].setVisible(state)
        self.widgets["emailField"].setVisible(state)
        self.widgets["passText"].setVisible(state)
        self.widgets["passField"].setVisible(state)

    def get(self):
        self.mainWorker.start()
        log("complete!")