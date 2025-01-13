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

def log(string):
    time = datetime.now()
    print("{}:{}:{} ; {}".format(time.hour,time.minute,time.second,string))