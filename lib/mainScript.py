from seleniumbase import Driver
from datetime import datetime
import time, json
import lib.misc as misc
import lib.webpages as wpage

with open("configs/objectLocations.json","r") as f: #loads xpaths and classes
    objectLocations = json.load(f)

with open("configs/loginInfo.json","r") as f:
    accountInfoAuto = json.load(f)


log = misc.log #logging method

def main(headless,browserHeadless,days,accountInfo=accountInfoAuto,displayMessageMethod=None, savePath = None, mainPageMethod=None, selectOrdersMethod=None, getOrdersMethod=None, fileType="json"): #days -1 will ask the user, should be defualt. headless means no gui
    if displayMessageMethod: displayMessageMethod("opening browser...")
    driver = Driver(uc=True, headless=browserHeadless) #main driver, the browser itself
    driver.uc_open_with_reconnect("https://www.doordash.com/orders", reconnect_time=3) #load orders page

    if driver.title == "Just a moment...": #if captcha loaded
        if browserHeadless:
            driver.quit()
            raise RuntimeError("captcha recieved! you cannot run in headless mode") #tell you to run in normal mode to click the button
        else:
            if displayMessageMethod: displayMessageMethod("press the captcha button...") #tell user to press button
            log("captcha button showed") #log just that
            while driver.find_elements("xpath",objectLocations["login"]["email"]) == []: #while login page not loaded
                if driver.find_elements("xpath",objectLocations["login"]["unexpectedCRF"]): #check if crf error
                    driver.back() #if so go back a page (no clue why this works?)
                time.sleep(0.25) #wait a bit to check again

    if "identity" in driver.current_url: #if not logged in
        if displayMessageMethod:
            if accountInfo["autoLogin"]: displayMessageMethod("logging in...") #display logging ing
            else: displayMessageMethod("press enter in console once logged in")
        success = wpage.accounts.login(driver,accountInfo["autoLogin"],accountInfo["DDusername"],accountInfo["DDpassword"]) #log in
        if not success:
            driver.quit()
            if displayMessageMethod: displayMessageMethod("script failed!\ncant login, is there 2fa?",method=mainPageMethod)
            else: raise RuntimeError("script failed! cant login, is there 2fa?")
            return

    if displayMessageMethod: displayMessageMethod("waiting for page to load...") #waiting for history page
    driver.wait_for_element("xpath",objectLocations["historyPage"]["ordersList"]) #wait for orders list page to show up

    selecting = True #while selecting orders (loop becuase might need to load page multible times because of load more button)
    while selecting:
        time.sleep(3) #wait a bit
        log("history page loaded") #log

        orders = wpage.historyPage.getOrders(driver) #get all orders on main webpage

        if orders: #if there are orders in the list
            selecting, selectedOrders = misc.selectOrders(headless, days, orders, wpage.historyPage.loadMore, driver, selectOrdersMethod, getOrdersMethod) #get selected orders
        else: #empty list?
            driver.quit()
            if displayMessageMethod: displayMessageMethod("script failed!\nno orders found, or there\nis an order on the way",method=mainPageMethod)
            else: raise RuntimeError("script failed! no orders found, or there is an order on the way")
            return
    
    log("orders:")
    for order in selectedOrders: print(order["link"].replace("https://www.doordash.com/orders/","")) #print orders

    totalSpending = {} #totals
    spendingDetailed = {} #detailed info on each order
    i = 1
    for order in selectedOrders: #loop through all orders
        if displayMessageMethod: displayMessageMethod("loading receipt {}/{}".format(i,len(selectedOrders))) #log progress
        driver.get(order["link"]) #load page
        driver.wait_for_element("xpath",objectLocations["receipt"]["ordersContainer"],timeout=30) #wait for receipt to load
        log("receipt {} loaded".format(order["link"].replace("https://www.doordash.com/orders/","")))
        time.sleep(.5) #wait

        spending, date, orderDetailed = wpage.receiptPage.getSpending(driver) #gets spending of eadch person on the current order

        orderInfo = order["info"].split(" • ") #receipt info: date, total price, num of items, personal/business
        spendingDetailed[order["link"]] = {"financial":orderDetailed} #creates detailed dict for order
        spendingDetailed[order["link"]]["spending"] = spending #sets how much everyone spent
        spendingDetailed[order["link"]]["name"] = order["name"] #store name
        spendingDetailed[order["link"]]["numberOfItems"] = orderInfo[2] #number of items
        spendingDetailed[order["link"]]["date"] = date #date of order

        for person in spending: #for each person
            if person not in totalSpending: totalSpending[person] = spending[person] #add them to the totals if they arent there
            else: totalSpending[person] += spending[person] #add to the persons total if they are there
        i += 1

    print("\n\nfinal spending:")
    for person in totalSpending: print("{}: {}".format(person,"{:.2f}".format(totalSpending[person]))) #print total spending to console

    driver.quit() #close browser
    if savePath: #if output to file
        data = {
            "lastRan": datetime.now().strftime("%m/%d/%Y %H:%M"), #set last ran
            "spendings": totalSpending, #total spendings
            "orders": spendingDetailed #detailed spendings
        }
        misc.export(data, fileType, savePath) #export to path
    if displayMessageMethod:
        displayMessageMethod("script completed!\ndata saved.",method=mainPageMethod)
    return totalSpending, spendingDetailed #return values