import sys,json,time
from lib.misc import log, BasePage
from PySide6.QtCore import QThread, Qt, Slot, Signal, QEventLoop
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QWidget, QCheckBox, QSpinBox, QLineEdit, QScrollArea

with open("configs/loginInfo.json","r") as f:
    accountInfo = json.load(f)

class mainScriptWorker(QThread):
    update_message_signal = Signal(tuple)  # Signal to update the message
    orderSelectorSignal = Signal(list)

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
        if accInfo != accountInfo:
            with open("configs/loginInfo.json","w") as f: #loads xpaths and classes
                json.dump(accInfo,f)
            log("updated loginInfo.json")

        mScript.main(False, bHeadless, days, accountInfo=accInfo, displayMessageMethod=self.on_message_update, savePath="data/output.json",mainPageMethod=self.orderWindow.on_back, selectOrdersMethod=self.orderSelector, getOrdersMethod=self.orderWindow.selectOrdersPage.get)
    
    def on_message_update(self, message, method=None):
        self.update_message_signal.emit((message,method))
    def orderSelector(self, orders):
        self.orderSelectorSignal.emit(orders)

class OrdersPage(BasePage):
    def __init__(self, container_widget: QStackedWidget, on_back: callable, dispMessage: callable, selectOrdersPage):
        super().__init__(container_widget)

        self.on_back = on_back
        self.dispMessageMethod = dispMessage
        self.selectOrdersPage = selectOrdersPage
        self.mainWorker = mainScriptWorker(self)
        self.mainWorker.update_message_signal.connect(self.dispMessage)
        self.mainWorker.orderSelectorSignal.connect(self.selectOrdersPage.display)

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

class orderSelector(BasePage):
    def __init__(self, container_widget: QStackedWidget):
        super().__init__(container_widget)
        self.layout = QVBoxLayout(self.page)

        self.loadMorePressed = False
        self.continuePressed = False

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Container widget inside scroll area
        self.scrollContainer = QWidget()
        self.scroll_layout = QVBoxLayout(self.scrollContainer)

        # Set up the scroll area
        self.scroll_area.setWidget(self.scrollContainer)
        self.layout.addWidget(self.scroll_area)

        #self.scroll_layout.addStretch()
        self.scroll_area.setWidget(self.scrollContainer)

        #self.layout.addStretch()
        self.button_layout = QHBoxLayout()
        self.loadButton = QPushButton("load more")
        self.continueButton = QPushButton("continue")
        self.loadButton.clicked.connect(self.loadMoreMethod)
        self.continueButton.clicked.connect(self.continueMethod)

        self.button_layout.addWidget(self.loadButton)
        self.button_layout.addWidget(self.continueButton)
        self.layout.addLayout(self.button_layout)
    
    def loadMoreMethod(self): self.loadMorePressed = True
    def continueMethod(self): self.continuePressed = True

    def display(self, orders):
        self.orders = orders
        self.loadMorePressed = False
        self.continuePressed = False
        print(self.continuePressed)

        # Clear the existing checkboxes
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.checkboxes = []
        for order in orders:
            text = "{},  {}".format(order["name"],order["info"])
            checkbox = QCheckBox(text)
            self.checkboxes.append(checkbox)
            self.scroll_layout.addWidget(checkbox)
        self.show()
        log("select order page displayed")

    def get(self):
        if self.loadMorePressed:
            log("pressed load more")
            self.loadMorePressed = False
            return False, True, []
        elif self.continuePressed:
            log("pressed continue, got orders")
            self.continuePressed = False
            selectedOrders = []
            for i in range(len(self.checkboxes)-1):
                if self.checkboxes[i].isChecked():
                    selectedOrders.append(self.orders[i])
            return False, False, selectedOrders
        else: return True, False, []