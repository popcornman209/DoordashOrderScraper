import time, json
from lib.misc import log

with open("configs/objectLocations.json","r") as f:
    objectLocations = json.load(f)

class accounts:
    def auioLogin(driver,usrname,passwd):
        if usrname == "" or passwd == "": raise ValueError("username and password must be filled out if using auto login!") #raise error
        driver.find_element("xpath", objectLocations["login"]["email"]).send_keys(usrname) #gets email text field and types email
        log("typed email")
        time.sleep(0.25)
        driver.find_element("xpath",objectLocations["login"]["signIn"]).click() #clicks sign in button
        log("started sign in")

        try: #if there is a "sign in with password instead" button
            driver.wait_for_element("xpath",objectLocations["login"]["passInstead"],timeout=2) #wait for sign in with pass instead button
            time.sleep(0.25)
            driver.find_element("xpath",objectLocations["login"]["passInstead"]).click() #click said button
            log("clicked use password instead")

            driver.wait_for_element("xpath",objectLocations["login"]["passwordWithInstead"]) #once on password page
            time.sleep(0.25)
            driver.find_element("xpath",objectLocations["login"]["passwordWithInstead"]).send_keys(passwd) #type password
        except: #if brought straight to password page
            log("no use password instead button.")

            driver.wait_for_element("xpath",objectLocations["login"]["passwordNoInstead"]) #wait for password field
            time.sleep(0.25)
            driver.find_element("xpath",objectLocations["login"]["passwordNoInstead"]).send_keys(passwd)  #type in said field
        log("typed pass")
        
        time.sleep(0.25)
        try:
            driver.find_element("xpath",objectLocations["login"]["signInFinal"]).click() #click sign in button
            log("pressed sign in button")
            return True
        except:
            return False
    
    def login(driver,autoLogin,usr,passw):
        log("reached login window...")
        if autoLogin: #if fill in email and password automatically
            return(accounts.auioLogin(driver,usr,passw))
        else: #if not fill in email automatically
            input("press enter when logged in and on orders page")
            return True

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
                info = order.find_element("xpath", objectLocations["historyPage"]["informationLocal"]).text #gets order info like date, price, and personal/business

                links.append({ #orders dictionary
                    "name": name,
                    "info": info,
                    "link": link
                })
        return links

    def loadMore(driver):
        log("loaded more history")
        loadMoreButton = driver.find_element("xpath", objectLocations["historyPage"]["loadMore"]) #finds and presses load more button
        loadMoreButton.click()

class receiptPage:
    def getSpending(driver):
        date = driver.find_element("xpath", objectLocations["receipt"]["date"]).text.replace(" at ",", ")

        ordersContainer = driver.find_element("xpath", objectLocations["receipt"]["ordersContainer"]) #gets container of each persons orders
        orders = ordersContainer.find_elements("xpath", "./div") #each persons orders
        detailedInfoContainer = orders[-1].find_element("xpath", "./div") #container of subtotals
        orders.pop() #removes "total" div

        detailedOrderData = {}
        for data in detailedInfoContainer.find_elements("xpath", "./div"): #for each subtotal in subtotals
            key = data.find_element("xpath", objectLocations["receipt"]["detailedInfoKey"]).text #get the name
            val = data.find_element("xpath", objectLocations["receipt"]["detailedInfoVal"]).text #get the value
            if "\n" in val: val = val.split("\n")[1] #if it was crossed out for whatever reason fix that
            detailedOrderData[key] = val #add it to the list
        log(detailedOrderData)
        

        spending = {}
        for order in orders:
            items = order.find_elements("xpath", "./div") #each persons orders
            items.pop(0)
            
            price = 0
            for item in items:
                price += round(float(item.find_element("xpath", objectLocations["receipt"]["priceLocal"]).text[1:]),2) #gets how much they spent

            person = order.find_element("xpath", objectLocations["receipt"]["nameLocal"]).text #gets person
            if person not in spending: spending[person] = price #adds them to the list if they arent already
            else: spending[person] += price #if they are there then add to their total (not sure why i added this?)
        return spending, date, detailedOrderData