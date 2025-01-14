import sys,json
from lib.misc import log
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QWidget, QCheckBox, QSpinBox, QLineEdit

with open("configs/loginInfo.json","r") as f: #loads xpaths and classes
    accountInfo = json.load(f)


class BasePage:
    def __init__(self, container_widget: QStackedWidget):
        self.page = QWidget()
        self.container_widget = container_widget

    def show(self): # Switch to this page in the stacked widget.
        self.container_widget.setCurrentWidget(self.page)


class OrdersPage(BasePage):
    def __init__(self, container_widget: QStackedWidget, on_back: callable):
        super().__init__(container_widget)

        main_layout = QVBoxLayout(self.page)

        self.widgets = {
            "headLessBrowser": QCheckBox("headless (hide browser window)"), #headless browser checkbox
            "manuallySelectOrders": QCheckBox("manually select orders"), #wether to manuall select orders
            "daysInPastText": QLabel("days to get in past:"), #text for following text field
            "daysInPastField": QSpinBox(), #days in past text field
            "autoLogin": QCheckBox("auto login (required if headless)"), #auto login check box
            "emailText": QLabel("email/username:"), #email: text
            "emailField": QLineEdit(accountInfo["DDusername"]), #email field
            "passText": QLabel("password:"), #password: text
            "passField": QLineEdit(accountInfo["DDpassword"]) #password field
        }
        
        for widget in self.widgets:
            main_layout.addWidget(self.widgets[widget], alignment=Qt.AlignHCenter) #puts all of the widgets in the layout
        
        self.widgets["manuallySelectOrders"].setCheckState(Qt.Checked) #set manual checkbox to true by default
        self.widgets["manuallySelectOrders"].stateChanged.connect(self.manualCheckBoxChanged) #toggle days in past objects when swithed
        self.manualCheckBoxChanged(True) #hide said objects

        self.widgets["daysInPastField"].setValue(7) #sets default value for days in past
        self.widgets["daysInPastField"].setRange(0, 364) #sets minimum

        if accountInfo["autoLogin"]: self.widgets["autoLogin"].setCheckState(Qt.Checked) #if autologin setting on, set on by default
        else: self.loginCheckBoxChanged(False) #otherwise hide other objects
        self.widgets["autoLogin"].stateChanged.connect(self.loginCheckBoxChanged) #toggles login objects when autologin switched
        self.widgets["emailField"].setFixedWidth(250) #fixed width for email field
        self.widgets["passField"].setEchoMode(QLineEdit.Password) #hide password
        self.widgets["passField"].setFixedWidth(250) #fixed width for password field

        main_layout.addStretch()

        # Add back and get buttons
        button_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        get_button = QPushButton("Get")
        back_button.clicked.connect(on_back)

        button_layout.addWidget(back_button)
        button_layout.addWidget(get_button)
        main_layout.addLayout(button_layout)
    
    def manualCheckBoxChanged(self,state):
        self.widgets["daysInPastText"].setVisible(state == False)
        self.widgets["daysInPastField"].setVisible(state == False)
    def loginCheckBoxChanged(self,state):
        self.widgets["emailText"].setVisible(state)
        self.widgets["emailField"].setVisible(state)
        self.widgets["passText"].setVisible(state)
        self.widgets["passField"].setVisible(state)


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
        self.orders_page = OrdersPage(self.stacked_widget, self.showMainPage)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.main_page.page)
        self.stacked_widget.addWidget(self.orders_page.page)

        log("GUI open")

    def showMainPage(self): self.main_page.show()
    def showOrdersPage(self): self.orders_page.show()


def run():
    log("Starting GUI...")
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
