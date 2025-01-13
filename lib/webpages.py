import time, json
from lib.misc import log

with open("configs/objectLocations.json","r") as f:
    objectLocations = json.load(f)

class accounts:
    def auioLogin(driver,usrname,passwd):
        driver.find_element("xpath", objectLocations["login"]["email"]).send_keys(usrname)
        log("typed email")
        time.sleep(0.25)
        driver.find_element("xpath",objectLocations["login"]["signIn"]).click()
        log("started sign in")

        try:
            driver.wait_for_element("xpath",objectLocations["login"]["passInstead"],timeout=2)
            time.sleep(0.25)
            driver.find_element("xpath",objectLocations["login"]["passInstead"]).click()
            log("clicked use password instead")

            driver.wait_for_element("xpath",objectLocations["login"]["passwordWithInstead"])
            time.sleep(0.25)
            driver.find_element("xpath",objectLocations["login"]["passwordWithInstead"]).send_keys(passwd)
        except:
            log("no use password instead button.")

            driver.wait_for_element("xpath",objectLocations["login"]["passwordNoInstead"])
            time.sleep(0.25)
            driver.find_element("xpath",objectLocations["login"]["passwordNoInstead"]).send_keys(passwd)
        log("typed pass")
        

        time.sleep(0.25)
        driver.find_element("xpath",objectLocations["login"]["signInFinal"]).click()
        log("pressed sign in button")
    
    def login(driver,autoLogin,usr,passw):
        log("reached login window...")
        if autoLogin == "automatic":
            accounts.auioLogin(driver,usr,passw)
        elif autoLogin == "manual":
            input("press enter when logged in and on orders page")
        else:
            raise ValueError("autoLogin can only be manual, automatic, or cookies!")

class historyPage:
    def getOrders(driver):
        parent_div = driver.find_element("xpath", objectLocations["historyPage"]["ordersList"]) #container of all orders
        orders = parent_div.find_elements("xpath", "./div") #list of orders

        links = []
        for order in orders:
            nameContainer = order.find_element("xpath", objectLocations["historyPage"]["nameContainerLocal"])
            nameContainerItems = nameContainer.find_elements("xpath", "./span") #container of name and group order tag
            if len(nameContainerItems) == 3: #if group order,
                receiptButton = order.find_element("xpath",objectLocations["historyPage"]["receiptLocal"]) #button that links to the receipt
                link = receiptButton.get_attribute("href") #the link

                name = nameContainerItems[0].text #name
                info = order.find_element("xpath", objectLocations["historyPage"]["informationLocal"]).text

                links.append({
                    "name": name,
                    "info": info,
                    "link": link
                })
        return links

    def loadMore(driver):
        loadMoreButton = driver.find_element("xpath", objectLocations["historyPage"]["loadMore"])
        loadMoreButton.click()

class receiptPage:
    def getSpending(driver):
        ordersContainer = driver.find_element("xpath", objectLocations["receipt"]["ordersContainer"])
        orders = ordersContainer.find_elements("xpath", "./div")
        orders.pop()

        spending = {}
        for order in orders:
            person = order.find_element("xpath", objectLocations["receipt"]["nameLocal"]).text
            price = float(order.find_element("xpath", objectLocations["receipt"]["priceLocal"]).text[1:])
            if person not in spending: spending[person] = price
            else: spending[person] += price
        return spending
