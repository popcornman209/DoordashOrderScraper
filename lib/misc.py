import pickle
from datetime import datetime

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

def selectOrders(headless, days, loadMoreMethod):
    if days == -1:
        if headless:
            print(("\033c\033[3J" if headless else "\n")+"orders:") 
            for i in range(len(orders)-1): print("{}: {}, {} ({})".format(i+1,orders[i]["name"],orders[i]["info"],orders[i]["link"])) #prints orders
            usedOrders = input('\nwhich orders would you like to count? (seperated by ",", or type "load" to load more)\n: ') #gets list of orders
            if usedOrders == "load": loadMoreMethod(driver) #load more
            else:
                selectedOrders = []
                for order in usedOrders.split(","): #get all selected orders
                    selectedOrders.append(orders[int(order)-1]) #add them to the list
                return False, selectedOrders
        else:
            return False, orders[:4] # TEMP
    else:
        return False, orders[:4] # TEMP

def log(string):
    time = datetime.now()
    print("{}:{}:{} ; {}".format(time.hour,time.minute,time.second,string))