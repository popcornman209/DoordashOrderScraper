from seleniumbase import Driver
import time, json
import lib.misc as misc
import lib.webpages as wpage

with open("configs/objectLocations.json","r") as f: #loads xpaths and classes
    objectLocations = json.load(f)

with open("configs/loginInfo.json","r") as f: #loads xpaths and classes
    accountInfo = json.load(f)


log = misc.log #logging method

def main(headless,browserHeadless,days): #days -1 will ask the user, should be defualt. headless means no gui
    driver = Driver(uc=True, headless=browserHeadless) #main driver, the browser itself
    driver.uc_open_with_reconnect("https://www.doordash.com/orders", reconnect_time=3) #load orders page


    if "identity" in driver.current_url: #if not logged in
        wpage.accounts.login(driver,accountInfo["autoLogin"],accountInfo["DDusername"],accountInfo["DDpassword"]) #log in


    driver.wait_for_element("xpath",objectLocations["historyPage"]["ordersList"]) #wait for orders list page to show up

    selecting = True
    while selecting:
        time.sleep(3) #wait a bit
        log("history page loaded") #log

        orders = wpage.historyPage.getOrders(driver) #get all orders on main webpage

        selecting, selectedOrders = misc.selectOrders(headless, days, orders, wpage.historyPage.loadMore)
    
    log("orders:")
    for order in selectedOrders: print(order["link"].replace("https://www.doordash.com/orders/","")) #print orders

    totalSpending = {}
    spendingDetailed = {}
    for order in selectedOrders: #loop through all orders
        driver.get(order["link"]) #load page
        driver.wait_for_element("xpath",objectLocations["receipt"]["ordersContainer"]) #wait for receipt to load
        log("receipt {} loaded".format(order["link"].replace("https://www.doordash.com/orders/","")))
        time.sleep(.5) #wait

        spending = wpage.receiptPage.getSpending(driver) #gets spending of eadch person on the current order

        spendingDetailed[order["link"]] = spending

        for person in spending: #for each person
            if person not in totalSpending: totalSpending[person] = spending[person] #add them to the totals if they arent there
            else: totalSpending[person] += spending[person] #add to the persons total if they are there

    print("\n\nfinal spending:")
    for person in totalSpending: print("{}: {}".format(person,"{:.2f}".format(totalSpending[person]))) #print total spending to console

    return totalSpending, spendingDetailed #return values