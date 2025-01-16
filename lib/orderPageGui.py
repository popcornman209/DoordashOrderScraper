import sys,json,time
from lib.misc import log, BasePage
from PySide6.QtCore import QThread, Qt, Slot, Signal, QEventLoop
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QWidget, QCheckBox, QSpinBox, QLineEdit, QScrollArea

with open("configs/loginInfo.json","r") as f:
    accountInfo = json.load(f)

class mainScriptWorker(QThread):
    update_message_signal = Signal(tuple)  # Signal to update the message
    orderSelectorSignal = Signal(list) #order selector page signal

    def __init__(self, orderWindow):
        super().__init__()
        self.orderWindow = orderWindow #order window, for getting parameters

    def run(self):
        import lib.mainScript as mScript
        bHeadless = self.orderWindow.widgets["headLessBrowser"].isChecked() #if to run browser in headless mode
        days = self.orderWindow.widgets["daysField"].value() if self.orderWindow.widgets["autoSelectOrders"].isChecked() else -1 #amount of days in the past, -1 if manual
        accInfo = { #account info dict
            "autoLogin": self.orderWindow.widgets["autoLogin"].isChecked(),
            "DDusername": self.orderWindow.widgets["emailField"].text(),
            "DDpassword": self.orderWindow.widgets["passField"].text()
        }
        if accInfo != accountInfo: #if there where changes
            with open("configs/loginInfo.json","w") as f: #save said changes
                json.dump(accInfo,f)
            log("updated loginInfo.json")

        #main script
        mScript.main(False, bHeadless, days, accountInfo=accInfo, displayMessageMethod=self.on_message_update, savePath="data/output.json",mainPageMethod=self.orderWindow.on_back, selectOrdersMethod=self.orderSelector, getOrdersMethod=self.orderWindow.selectOrdersPage.get)
    
    def on_message_update(self, message, method=None):
        self.update_message_signal.emit((message,method)) #display message method
    def orderSelector(self, orders):
        self.orderSelectorSignal.emit(orders) #select orders page

class OrdersPage(BasePage):
    def __init__(self, container_widget: QStackedWidget, on_back: callable, dispMessage: callable, selectOrdersPage):
        super().__init__(container_widget)

        self.on_back = on_back #back to main menu
        self.dispMessageMethod = dispMessage #display message method
        self.selectOrdersPage = selectOrdersPage #page for selecting orders
        self.mainWorker = mainScriptWorker(self) #main worker, runs the script in seperate thread
        self.mainWorker.update_message_signal.connect(self.dispMessage) #connecting signals
        self.mainWorker.orderSelectorSignal.connect(self.selectOrdersPage.display) #^^

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

        main_layout.addStretch() #sctretch to put buttons at bottom

        # Add back and get buttons
        button_layout = QHBoxLayout() #horizontal box for two buttons
        back_button = QPushButton("back")
        get_button = QPushButton("continue")
        back_button.clicked.connect(self.on_back) #back to main menu button
        get_button.clicked.connect(self.get) #run button

        button_layout.addWidget(back_button)
        button_layout.addWidget(get_button)
        main_layout.addLayout(button_layout)
    
    def dispMessage(self,data):
        self.dispMessageMethod(data[0],method=data[1]) #displays message on screem, and can have buttons
    def manualCheckBoxChanged(self,state): #toggles days field depending on wether doing it manually or not
        self.widgets["daysText"].setVisible(state)
        self.widgets["daysField"].setVisible(state)
    def loginCheckBoxChanged(self,state): #if logging in manually, hide login info
        self.widgets["emailText"].setVisible(state)
        self.widgets["emailField"].setVisible(state)
        self.widgets["passText"].setVisible(state)
        self.widgets["passField"].setVisible(state)

    def get(self): #run main script
        log("starting script...")
        self.mainWorker.start()

class orderSelector(BasePage):
    def __init__(self, container_widget: QStackedWidget):
        super().__init__(container_widget)
        self.layout = QVBoxLayout(self.page)

        self.loadMorePressed = False #two variables for if button was pressed or not
        self.continuePressed = False

        self.scroll_area = QScrollArea() #scroll area, where checkboxes go
        self.scroll_area.setWidgetResizable(True)

        self.scrollContainer = QWidget()
        self.scroll_layout = QVBoxLayout(self.scrollContainer) #stores all checkboxes

        # Set up the scroll area
        self.scroll_area.setWidget(self.scrollContainer)
        self.layout.addWidget(self.scroll_area)

        self.scroll_area.setWidget(self.scrollContainer)

        self.button_layout = QHBoxLayout()
        self.loadButton = QPushButton("load more") #load more orders
        self.continueButton = QPushButton("continue") #continue and submit
        self.loadButton.clicked.connect(self.loadMoreMethod)
        self.continueButton.clicked.connect(self.continueMethod)

        self.button_layout.addWidget(self.loadButton)
        self.button_layout.addWidget(self.continueButton)
        self.layout.addLayout(self.button_layout)
    
    def loadMoreMethod(self): self.loadMorePressed = True #sets either flag to be true, used for get method
    def continueMethod(self): self.continuePressed = True

    def display(self, orders):
        self.orders = orders #sets list of orders
        self.loadMorePressed = False #resets arguments
        self.continuePressed = False

        # Clear the existing checkboxes
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.checkboxes = [] #set list of checkboxes to be empty
        for order in orders: #loop through each order
            text = "{},  {}".format(order["name"],order["info"])
            checkbox = QCheckBox(text) #make a checkbox for the order
            self.checkboxes.append(checkbox) #add checkbox to list
            self.scroll_layout.addWidget(checkbox) #add checkbox to screen
        self.show() #display page
        log("select order page displayed")

    def get(self): #get which button was pressed, if either
        if self.loadMorePressed: #if load more was pressed
            log("pressed load more")
            self.loadMorePressed = False #reset argument
            return False, True, [] #return "stop checking, load more, blank list"
        elif self.continuePressed: #if continue button was pressed
            log("pressed continue, got orders")
            self.continuePressed = False #reset argument
            selectedOrders = [] #reset selected orders list
            for i in range(len(self.checkboxes)-1):
                if self.checkboxes[i].isChecked():
                    selectedOrders.append(self.orders[i]) #loop through each checkbox, and add an order to the list if it was selected
            return False, False, selectedOrders #return "stop checking, dont load more, list of selected orders"
        else: return True, False, [] #return "keep checking, dont load more, empty list"