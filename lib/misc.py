import pickle
from datetime import datetime, timedelta
from PySide6.QtWidgets import QStackedWidget, QWidget

class BasePage:
    def __init__(self, container_widget: QStackedWidget):
        self.page = QWidget()
        self.container_widget = container_widget

    def show(self): # Switch to this page in the stacked widget.
        self.container_widget.setCurrentWidget(self.page)

class cookies:
    cookieFile = "data/cookies.pkl"

    def saveCookies(driver):
        cookies = [cookie for cookie in driver.get_cookies() if "doordash" in cookie["domain"]]
        with open(cookies.cookieFile, "wb") as f:
            pickle.dump(cookies, f)

    def loadCookies(driver):
        with open(cookies.cookieFile, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            if "domain" in cookie and not cookie["domain"].endswith("doordash.com"):
                del cookie["domain"]
            driver.add_cookie(cookie)

def getDate(order):
    parsed = order["info"].split(" • ")
    return parsed[0]

def isDateInRange(date_str, days):
    current_date = datetime.now()

    date_str_with_year = f"{current_date.year}, {date_str}" # Add the current year to the date string

    date_format = "%Y, %a, %b %d" # Parse the date string into a datetime object, including the year
    date_obj = datetime.strptime(date_str_with_year, date_format)

    if date_obj > current_date: # If the date is after today, adjust it to the previous year
        date_obj = date_obj.replace(year=current_date.year - 1)

    past_date = current_date - timedelta(days=days) # Calculate the date x days ago

    return past_date <= date_obj <= current_date # Check if the date is within the last x days

def selectOrders(headless, days, orders, loadMoreMethod, driver):
    if days == -1:
        if headless:
            print("\n\norders:") 
            for i in range(len(orders)-1): print("{}: {}, {} ({})".format(i+1,orders[i]["name"],orders[i]["info"],orders[i]["link"])) #prints orders
            usedOrders = input('\nwhich orders would you like to count? (seperated by ",", or type "load" to load more)\n: ') #gets list of orders
            if usedOrders == "load":
                loadMoreMethod(driver) #load more
                return True, []
            else:
                selectedOrders = []
                for order in usedOrders.split(","): #get all selected orders
                    selectedOrders.append(orders[int(order)-1]) #add them to the list
                return False, selectedOrders
        else:
            return False, orders[:4] # TEMP
    else:
        if isDateInRange(getDate(orders[-1]),days):
            loadMoreMethod(driver)
            return True, []
        else:
            selectedOrders = []
            for order in orders:
                if isDateInRange(getDate(order),days): selectedOrders.append(order)
            return False, selectedOrders

def log(string):
    time = datetime.now()
    print("{}:{}:{} ; {}".format(time.hour,time.minute,time.second,string))